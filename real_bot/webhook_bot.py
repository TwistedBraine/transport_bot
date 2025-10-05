# -*- coding: utf-8 -*-
import os
import logging
from flask import Flask, request, render_template
import telebot

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Получаем токен из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN не найден в переменных окружения")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# Импортируем обработчики
try:
    from handlers.start import setup_start_handlers
    from handlers.register import setup_register_handlers
    from handlers.search import setup_search_handlers
    from handlers.phones import setup_phones_handlers
    from handlers.weather import setup_weather_handlers
    from handlers.other import setup_other_handlers
    from handlers.mechanics import setup_mechanics_handlers
    from handlers.fuel import setup_fuel_handlers
    from handlers.admin import setup_admin_handlers

    # Настраиваем обработчики
    setup_start_handlers(bot)
    setup_register_handlers(bot)
    setup_search_handlers(bot)
    setup_phones_handlers(bot)
    setup_weather_handlers(bot)
    setup_other_handlers(bot)
    setup_mechanics_handlers(bot)
    setup_fuel_handlers(bot)
    setup_admin_handlers(bot)

    logger.info("✅ Все обработчики настроены")

except Exception as e:
    logger.error(f"❌ Ошибка настройки обработчиков: {e}")
    exit(1)

# WEB APP МАРШРУТЫ
@app.route("/webapp")
def webapp():
    """Основной Web App интерфейс"""
    return render_template('webapp.html')

@app.route("/webapp/test")
def webapp_test():
    """Тестовая страница Web App"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Тест Web App</title>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <style>
            body {
                font-family: Arial, sans-serif;
                padding: 20px;
                text-align: center;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                margin: 0;
            }
            .container {
                max-width: 400px;
                margin: 0 auto;
                padding-top: 50px;
            }
            button {
                background: white;
                color: #667eea;
                border: none;
                padding: 12px 25px;
                border-radius: 20px;
                font-size: 16px;
                cursor: pointer;
                margin: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚍 ШЕСТОЕ ЭЛЕКТРИЧЕСТВО</h1>
            <p>✅ Web App тест работает!</p>
            <button onclick="Telegram.WebApp.close()">Закрыть</button>
        </div>
        <script>
            Telegram.WebApp.ready();
            Telegram.WebApp.expand();
        </script>
    </body>
    </html>
    """

# WEBHOOK МАРШРУТ
@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработка webhook от Telegram"""
    logger.info("📨 Получено сообщение от Telegram")
    try:
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)

        if update.message:
            logger.info(f"👤 Сообщение от {update.message.from_user.id}: {update.message.text}")

        # Обрабатываем сообщение
        bot.process_new_updates([update])
        logger.info("✅ Сообщение обработано ботом")
        return "!", 200

    except Exception as e:
        logger.error(f"❌ Ошибка: {e}", exc_info=True)
        return "Error", 500

# СТРАНИЦЫ
@app.route("/")
def index():
    return "🚍 Транспортный бот работает! Web App: /webapp"

@app.route("/health")
def health():
    return "OK", 200

@app.route("/setup_webhook")
def setup_webhook():
    """Установка webhook (вызвать один раз после деплоя)"""
    webhook_url = f'https://{request.host}/webhook'
    result = bot.set_webhook(url=webhook_url)
    return f"Webhook установлен: {webhook_url} - {result}"

# ЗАПУСК СЕРВЕРА
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)