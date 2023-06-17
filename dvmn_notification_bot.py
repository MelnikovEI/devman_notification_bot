import argparse
import textwrap
from time import sleep
import requests
from environs import Env
import telegram
import logging
from retry import retry

logger = logging.getLogger(__file__)


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    @retry(telegram.error.NetworkError, delay=1, backoff=2, tries=10, max_delay=30, logger=logger)
    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


@retry(telegram.error.TimedOut, delay=1, backoff=2, max_delay=30, tries=10, logger=logger)
def send_tg_notification(bot, chat_id, tg_message):
    bot.send_message(chat_id=chat_id, text=tg_message)


def main():
    env = Env()
    env.read_env()
    devman_access_token = env('DEVMAN_ACCESS_TOKEN')
    tg_bot_token = env('TG_BOT_TOKEN')
    tg_user_id = env('TG_USER_ID')

    bot = telegram.Bot(token=tg_bot_token)

    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(bot, tg_user_id))
    logger.info("Бот запущен")

    headers = {'Authorization': f'Token {devman_access_token}'}
    params = {}

    while True:
        try:
            try:
                dvmn_response = requests.get("https://dvmn.org/api/long_polling/", headers=headers, timeout=90,
                                             params=params)
                dvmn_response.raise_for_status()
                dvmn_check_list = dvmn_response.json()
            except requests.exceptions.ReadTimeout:
                logger.debug("requests ReadTimeout, повторяю запрос")
                continue
            except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
                logger.info("requests ConnectionError or ConnectTimeout, повторяю запрос")
                sleep(15)
                continue
            if dvmn_check_list['status'] == 'found':
                params['timestamp'] = dvmn_check_list['last_attempt_timestamp']
                tg_message = textwrap.dedent(
                    f'''Преподаватель проверил работу "{dvmn_check_list["new_attempts"][0]["lesson_title"]}".
{dvmn_check_list["new_attempts"][0]["lesson_url"]}'''
                )
                if dvmn_check_list['new_attempts'][0]['is_negative']:
                    tg_message += "\nК сожалению, в работе нашлись ошибки :("
                else:
                    tg_message += "\nПреподавателю всё понравилось, можно приступать к следующему уроку!"
                send_tg_notification(bot, tg_user_id, tg_message)
            if dvmn_check_list['status'] == 'timeout':
                params['timestamp'] = dvmn_check_list['timestamp_to_request']
        except Exception as err:
            logger.error(err)
            sleep(15)


if __name__ == '__main__':
    main()
