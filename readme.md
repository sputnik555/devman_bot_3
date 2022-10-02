## Бот онлайн издательства «Игра глаголов»
Бот предназначен для ответов на частые вопросы пользователей в Telegram и VK.

### Переменные окружения
Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` и
запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны следующие переменные:
- `TELEGRAM_TOKEN` — Токен основного Telegram-бота
- `TELEGRAM_LOGGER_TOKEN` - Токен Telegram-бота для логирования
- `TG_LOGGER_CHAT_ID` - ID чата, в который будут отправляться сообщения ботом логирования. Можно получить у бота `@userinfobot`
- `GOOGLE_APPLICATION_CREDENTIALS` - Путь к файлу .json, содержащему реквизиты авторизации GOOGLE API. [Подробнее](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating)
- `GOOGLE_PROJECT_NAME` - Имя проекта DialogFlow в GOOGLE cloud. [Подробнее](https://cloud.google.com/dialogflow/es/docs/quick/setup)
- `VK_TOKEN` - Токен VK-бота

### Обучение бота
В проект DataFlow, который используется ботом, можно загрузить базу вопросов и ответов из файла .json, для этого 
предназначен скрипт `import_intents.py`
Необходимо создать файл questions.json в папке проекта, имеющий следующую структуру:
```json
{
  "Устройство на работу": {
    "questions": [
      "Как устроиться к вам на работу?",
      "Как устроиться к вам?",
      "Как работать у вас?",
      "Хочу работать у вас",
      "Возможно-ли устроиться к вам?",
      "Можно-ли мне поработать у вас?",
      "Хочу работать редактором у вас"
    ],
    "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
  },
  ...
}
```
Затем запустить скрипт `import_intents.py`:
```commandline
python import_intents.py
```

### Запуск бота
Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:
```bash
pip install -r requirements.txt
```

Для запуска скрипта необходимо выполнить в консоли следующие команды:
1. Для запуска Telegram-бота
```bash
python tg_bot.py
```
2. Для запуска VK-бота
```bash
python vk_bot.py
```