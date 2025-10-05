# -*- coding: utf-8 -*-
from database import user_db

def send_message_with_cleanup(bot, user_id, chat_id, text, reply_markup=None, log_action=None, parse_mode=None):
    """Отправляет сообщение, предварительно удаляя предыдущие сообщения бота и пользователя"""
    try:
        # Удаляем предыдущее сообщение бота
        user_db.delete_last_bot_message(bot, user_id, chat_id)
        
        # Удаляем ВСЕ сообщения пользователя
        user_db.delete_user_messages(bot, user_id, chat_id)
        
    except Exception as e:
        print(f"⚠️ Ошибка удаления сообщений: {e}")
    
    # Логируем действие если указано
    if log_action:
        try:
            user_db.log_usage(user_id, "User", log_action)
        except Exception as e:
            print(f"⚠️ Ошибка логирования: {e}")
    
    # Отправляем новое сообщение
    sent_message = bot.send_message(
        chat_id,
        text,
        reply_markup=reply_markup,
        parse_mode=parse_mode
    )
    
    # Сохраняем ID нового сообщения бота
    try:
        user_db.save_last_bot_message(user_id, sent_message.message_id)
    except Exception as e:
        print(f"⚠️ Ошибка сохранения сообщения бота: {e}")
    
    return sent_message

def save_user_message(user_id, message_id, chat_id):
    """Сохраняет сообщение пользователя для последующего удаления"""
    try:
        result = user_db.save_user_message(user_id, message_id, chat_id)
        print(f"💾 Сохранено сообщение пользователя {user_id}: {message_id}")
        return result
    except Exception as e:
        print(f"❌ Ошибка сохранения сообщения пользователя: {e}")
        return False