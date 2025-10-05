# -*- coding: utf-8 -*-
import telebot
from database import user_db, employee_db
from keyboards import main_keyboard
from utils import send_message_with_cleanup, save_user_message

def setup_search_handlers(bot):
    @bot.message_handler(func=lambda m: m.text == '🔍 Поиск водителей')
    def handle_driver_search(message):
        user_id = message.from_user.id
        save_user_message(user_id, message.message_id, message.chat.id)
        
        if not user_db.is_registered(user_id):
            send_message_with_cleanup(
                bot, user_id, message.chat.id,
                "❌ Для доступа к поиску необходима регистрация.",
                main_keyboard(user_id),
                log_action="search_denied"
            )
            return
        
        if not user_db.can_search_drivers(user_id):
            send_message_with_cleanup(
                bot, user_id, message.chat.id,
                "❌ Доступ запрещен. Поиск доступен только сотрудникам компании.",
                main_keyboard(user_id),
                log_action="search_denied_not_employee"
            )
            return
        
        send_message_with_cleanup(
            bot, user_id, message.chat.id,
            "🔍 Введите данные для поиска:",
            main_keyboard(user_id),
            log_action="search_started"
        )
        bot.register_next_step_handler(message, process_driver_search)
    
    def process_driver_search(message):
        user_id = message.from_user.id
        save_user_message(user_id, message.message_id, message.chat.id)
        
        if message.text in ['🔍 Поиск водителей', '📞 Телефоны', '🚌 Маршруты', '🏥 Профосмотр', '🏢 Филиалы', '🌤️ Погода', '🔧 Текущий механик', '⛽ Расчет топлива', '📊 Статистика']:
            return
        
        drivers_data = employee_db.search_drivers(message.text)
        
        if not drivers_data:
            send_message_with_cleanup(
                bot, user_id, message.chat.id,
                "❌ Водители не найдены.",
                main_keyboard(user_id),
                log_action="search_no_results"
            )
        else:
            response = f"🔍 Найдено водителей: {len(drivers_data)}\n\n"
            for i, driver in enumerate(drivers_data[:10], 1):
                response += f"👤 {driver.get('name', '')} {driver.get('surname', '')}\n"
                response += f"📞 {driver.get('phone', '')}\n"
                response += f"🔢 Таб. {driver.get('id', '')}\n"
                response += f"🚍 Маршрут {driver.get('route', '')}\n\n"
            
            send_message_with_cleanup(
                bot, user_id, message.chat.id,
                response,
                main_keyboard(user_id),
                log_action="search_results"
            )