# Интеграция чат-ботов telegram и vk с сервисами Google Dialogflow

Приложение предназначено для ведения диалога с пользователями с помощью чат-ботов telegram и vk. Ответы формируются службами Google Dialogflow 

### Как установить

Скачайте код:
```sh
git clone https://github.com/dimsonnGH/Bot-recognition
```
Для работы необходим Python 3 версии. Если он у вас еще не установлен, [Установите отсюда](https://www.python.org/).

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```
Рекомендуется запускать приложение в виртуальном окружении. Чтобы его создать, выполните в каталоге проекта:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:
- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

### Настройка telegram-бота

Зарегистрируйте бота в Telegram. Для этого напишите [Отцу ботов](https://telegram.me/BotFather) команду `\start`, а затем `\newbot`. Отец ботов вернет токен доступа к API Telegram.

[Создайте проект в DialogFlow](https://cloud.google.com/dialogflow/docs/quick/setup)

[Создайте агента в DialogFlow ](https://cloud.google.com/dialogflow/docs/quick/build-agent)

[Получите API-токен DialogFlow](https://cloud.google.com/docs/authentication/api-keys)

[Включите API DialogFlow в Google-аккаунте](https://cloud.google.com/dialogflow/es/docs/quick/setup#api)

Получите файл с ключами от Google-аккаунта с помощью [консольной утилиты](https://cloud.google.com/dialogflow/es/docs/quick/setup#sdk)

Обучите DialogFlow с помощью запуска скрипта:
```sh
python create_intents.py <путь к файлу json с тренировочными фразами> 
```
В репозитории есть образец файла с тренировочными фразами - ```questions.json```

Для получения в Telegram сообщений об ошибках в работе ботов узнайте свой chat_id, для этого напишите в Telegram специальному боту: [@userinfobot](https://telegram.me/userinfobot)

Cоздате файл `.env` в каталоге проекта со следующими настройками:

```DVNM_BOT_TELEGRAM_TOKEN=<токен доступа к API Telegram>```
```GOOGLE_APPLICATION_CREDENTIALS=<путь к файлу .json с ключами Google>```
```GOOGLE_PROJECT_ID=<идентификатор проекта DialogFlow>```
```GOOGLE_API_KEY=<API-токен DialogFlow>```
```TELEGRAM_CHAT_ID=<chat_id в Telegram>```
### Запуск telegram-бота

Запустите telegram-бота 
```sh
python telegram_bot.py 
```
Проверьте работу telegram-бота.

### Настройка vk-бота
Создайте группу Вконтакте.

Разрешите боту отправлять сообщения от имени группы ![Настройка отправки сообщений группы](https://dvmn.org/media/screenshot_from_2019-04-29_20-15-54.png "Настройка отправки сообщений группы") 

Получите [API токен группы](https://vk.com/dev/bots_docs).

Добавьте в файл `.env` в каталоге проекта со следующую настройку:
```VK_API_KEY=<API токен группы vk>```

### Запуск vk-бота

Запустите vk-бота 
```sh
python vk_bot.py 
```
Проверьте работу vk-бота, отправив сообщение в группу vk.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).