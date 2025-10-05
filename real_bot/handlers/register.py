# -*- coding: utf-8 -*-
import telebot
from database import user_db
from keyboards import main_keyboard
from utils import send_message_with_cleanup, save_user_message

def setup_register_handlers(bot):
    @bot.message_handler(content_types=['contact'])
    def handle_contact(message):
        user_id = message.from_user.id
        save_user_message(user_id, message.message_id, message.chat.id)
        
        if message.contact:
            phone = message.contact.phone_number
            username = message.from_user.first_name
            
            user_db.register_user(user_id, phone, username)
            
            send_message_with_cleanup(
                bot, user_id, message.chat.id,
                f"✅ Регистрация успешна!\n📱 Ваш номер: {phone}",
                main_keyboard(user_id)
            )
        else:
            send_message_with_cleanup(
                bot, user_id, message.chat.id,
                "❌ Не удалось получить номер.",
                main_keyboard(user_id)
            )