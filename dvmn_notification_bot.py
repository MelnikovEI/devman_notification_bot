import argparse
from time import sleep
import requests
from environs import Env
import telegram


def main():
    env = Env()
    env.read_env()
    devman_access_token = env('DEVMAN_ACCESS_TOKEN')
    tg_bot_token = env('TG_BOT_TOKEN')

    bot = telegram.Bot(token=tg_bot_token)

    parser = argparse.ArgumentParser(description='Telegram bot sends notifications about tasks control results')
    parser.add_argument("chat_id", help='You can get your id from https://t.me/userinfobot')
    args = parser.parse_args()
    chat_id = args.chat_id

    headers = {
        'Authorization': f'Token {devman_access_token}',
    }
    params = {}
    while True:
        try:
            dvmn_response = requests.get("https://dvmn.org/api/long_polling/", headers=headers, timeout=90,
                                         params=params)
            dvmn_response.raise_for_status()
        except requests.exceptions.ReadTimeout:
            continue
        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
            sleep(15)
            continue
        if dvmn_response.json()['status'] == 'found':
            params['timestamp'] = dvmn_response.json()['last_attempt_timestamp']
            bot.send_message(
                chat_id=chat_id,
                text=f'Преподаватель проверил работу "{dvmn_response.json()["new_attempts"][0]["lesson_title"]}".\n'
                     f'{dvmn_response.json()["new_attempts"][0]["lesson_url"]}'
            )
            if dvmn_response.json()['new_attempts'][0]['is_negative']:
                bot.send_message(chat_id=chat_id, text="К сожалению, в работе нашлись ошибки :(")
            else:
                bot.send_message(chat_id=chat_id,
                                 text="Преподавателю всё понравилось, можно приступать к следующему уроку!"
                                 )
        if dvmn_response.json()['status'] == 'timeout':
            params['timestamp'] = dvmn_response.json()['timestamp_to_request']


if __name__ == '__main__':
    main()
