# Отправляем уведомления о проверке работ
Телеграм бот уведомляет о результатах проверки работ на [dvmn.org](https://dvmn.org/)

## Как установить
Для запуска у вас уже должны быть установлены:
- [Python 3](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/desktop/)

Скачайте код скрипта, например:
```sh
git clone https://github.com/MelnikovEI/devman_notification_bot
```

Создайте бота в телеграм с помощью https://t.me/BotFather.  
Создайте файл с переменными окружения в папке проекта: "your_project_folder\\.env":
- DEVMAN_ACCESS_TOKEN= <- токен Вашего доступа к [API Devman](https://dvmn.org/api/docs/)  
- TG_BOT_TOKEN= <- токен бота можно узнать в https://t.me/BotFather
- TG_USER_ID= <- id учетной записи телеграм пользователя, которого нужно уведомлять, узнать: https://telegram.me/userinfobot

В командной строке войдите в папку проекта:
```sh
cd C:\Users\ ... \devman_notification_bot
```
Запустите [Docker Desktop](https://docs.docker.com/desktop/)  
Создайте докер-образ:
```sh
docker build --tag devman_notifications .
```
Пример успешного результата: `#12 DONE 0.4s`

## Как использовать
### Запустить бот:
```sh
docker run -d --env-file .env devman_notifications
```
### Проверить статус
```sh
docker ps
```
Пример результата:
```text
CONTAINER ID   IMAGE                      COMMAND                  CREATED         STATUS                   PORTS                    NAMES
96b55a8c6ae3   devman_notifications       "python3 dvmn_notifi…"   2 minutes ago   Up 2 minutes                                      agitated_mclean
3718060ba466   welcome-to-docker:latest   "docker-entrypoint.s…"   21 hours ago    Exited (0) 2 hours ago   0.0.0.0:8089->3000/tcp   naughty_austin
```
### Остановить бот:
```shell
docker stop agitated_mclean
```

### Результат работы:
Как только работа будет проверена, бот пришлёт Вам оповещение, например:

`Преподаватель проверил работу "Отправляем уведомления о проверке работ".
https://dvmn.org/modules/chat-bots/lesson/devman-bot/
К сожалению, в работе нашлись ошибки :(`

Такое же оповещение придёт, если Вы отзовете отправленную работу с проверки.

### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
### Authors
[Evgeny Melnikov](https://github.com/MelnikovEI)
