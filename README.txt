MyGymProgress — Mini App (Telegram) — ZIP-пакет
=============================================

Файлы в архиве:
- index.html           — frontend (Mini App) на русском
- app.py               — backend (Flask) + API endpoints (/api/init, /api/log) и /send_button
- requirements.txt     — зависимости Python
- README.txt           — эта инструкция
- database.db          — (не включен; создаётся автоматически при первом запуске)

Цель: развернуть приложение на Render (рекомендуется) или другом хостинге с Python 3.10+.

ШАГИ — пошагово (для новичка)
-----------------------------

1) Зарегистрируйся на Render: https://render.com (бесплатный аккаунт подходит).
2) Создай новый Web Service (Python):
   - Connect GitHub repository: можно загрузить этот ZIP в GitHub и выбрать репозиторий,
     либо на Render можно импортировать напрямую из архивов.
   - Build Command: leave empty or set to: pip install -r requirements.txt
   - Start Command: python app.py
3) Переменные окружения (Environment):
   - BOT_TOKEN = <твой токен от @BotFather>  (если хочешь, чтобы бот отправлял кнопку)
   - ADMIN_CHAT_ID = <твой numeric chat id> (узнать можно через @userinfobot)
   - PUBLIC_URL = https://your-app.onrender.com  (адрес, который выдаст Render)
   - PORT — можно не задавать (Render сам назначит)
4) После деплоя зайди в браузере на:
   https://<your-app>.onrender.com/send_button
   Это вызовет метод отправки сообщения от бота с кнопкой «Открыть MyGymProgress» в Telegram
   (бот отправит это сообщение в чат ADMIN_CHAT_ID).
5) В Telegram открой пришедшее сообщение и нажми "Открыть MyGymProgress" — Mini App откроется
   внутри Telegram, и ты сможешь добавлять тренировки.

Как получить ADMIN_CHAT_ID (numeric):
- В Telegram найди бота @userinfobot или @get_id_bot и нажми Start — он пришлёт твой numeric id.
- Вставь это число в Render → Environment → ADMIN_CHAT_ID.

Запуск локально (если хочешь проверить на компьютере):
1) Установи Python 3.10+.
2) Создай виртуальное окружение:
   python -m venv venv
   source venv/bin/activate   (mac/linux) или venv\Scripts\activate (Windows)
3) Установи зависимости:
   pip install -r requirements.txt
4) Запусти:
   python app.py
5) Открой в браузере http://127.0.0.1:5000 — увидишь страницу.
6) Чтобы бот пришлёт кнопку, тоже нужно задать BOT_TOKEN и ADMIN_CHAT_ID как переменные окружения,
   и в /send_button указать PUBLIC_URL (если локально, можно использовать ngrok для публичного URL).

Примечания и дальнейшие шаги:
- На первом этапе приложение полностью бесплатное — платёжные функции не включены.
- Когда будешь готов(а) к оплате — я помогу интегрировать платежи через Telegram Payments и включить контроль первых 50 пользователей бесплатно.
- Если хочешь, я могу прислать пошаговые скриншоты того, как заполнить поля на Render.

Если что-то сломается — напиши прямо здесь, укажи на каком шаге, и я помогу.

Удачи! — я подготовил ZIP, скачай ниже.