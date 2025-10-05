# -*- coding: utf-8 -*-
import telebot
from database import user_db
from keyboards import main_keyboard
from utils import send_message_with_cleanup, save_user_message

def is_admin(user_id):
    return user_id == 130123754

def setup_admin_handlers(bot):
    
    @bot.message_handler(commands=['myid'])
    def handle_myid(message):
        user_id = message.from_user.id
        save_user_message(user_id, message.message_id, message.chat.id)
        
        response = f"""🆔 ВАШ TELEGRAM ID

👤 Ваше имя: {message.from_user.first_name}
🔢 Ваш ID: `{user_id}`
{"👑 Статус: АДМИНИСТРАТОР" if is_admin(user_id) else "👤 Статус: пользователь"}"""
        
        send_message_with_cleanup(
            bot, user_id, message.chat.id,
            response,
            main_keyboard(user_id)
        )
    
    @bot.message_handler(func=lambda m: m.text == '📊 Статистика' and is_admin(m.from_user.id))
    def handle_stats(message):
        user_id = message.from_user.id
        save_user_message(user_id, message.message_id, message.chat.id)
        
        try:
            stats = user_db.get_stats()
            
            response = f"""📊 СТАТИСТИКА БОТА
Управление: Семенов Александр (таб. 2586)

——— 📈 ОБЩАЯ СТАТИСТИКА ———

👥 Всего пользователей: {stats['total_users']}
🔢 Всего действий: {stats['total_actions']}

——— 🏆 ПОПУЛЯРНЫЕ ДЕЙСТВИЯ ———"""

            for action, count in stats['popular_actions']:
                action_name = {
                    'admin_stats': '📊 Просмотр статистики',
                    'start': '🚀 Запуск бота',
                    'start_unregistered': '🚀 Запуск (незарегистрирован)',
                    'search_started': '🔍 Поиск (начало)',
                    'search_results': '🔍 Поиск (результаты)',
                    'search_drivers': '🔍 Поиск водителей', 
                    'current_mechanic': '🔧 Текущий механик',
                    'phones_menu': '📞 Меню телефонов',
                    'phones_park': '🏢 Телефоны парка',
                    'phones_management': '👔 Телефоны руководства',
                    'phones_glonass': '🛰️ Телефоны ГЛОНАСС',
                    'routes': '🚌 Маршруты',
                    'medical': '🏥 Профосмотр',
                    'branches': '🏢 Филиалы',
                    'weather': '🌤️ Погода',
                    'registration_success': '✅ Успешная регистрация'
                }.get(action, action)
                
                response += f"\n• {action_name}: {count}"
            
            response += "\n\n——— 👤 АКТИВНЫЕ ПОЛЬЗОВАТЕЛИ ———"
            
            for user, count in stats['active_users']:
                response += f"\n• {user}: {count} действий"
            
            response += "\n\n💡 Статистика обновляется в реальном времени"
            
            send_message_with_cleanup(
                bot, user_id, message.chat.id,
                response,
                main_keyboard(user_id)
            )
            
        except Exception as e:
            print(f"❌ Ошибка получения статистики: {e}")
            send_message_with_cleanup(
                bot, user_id, message.chat.id,
                "❌ Не удалось получить статистику.\nПопробуйте позже.",
                main_keyboard(user_id)
            )