# -*- coding: utf-8 -*-
import telebot
from datetime import datetime, timedelta
from keyboards import main_keyboard
from utils import send_message_with_cleanup, save_user_message

MECHANICS_SCHEDULE = {
    "night_1": {
        "name": "Шаповалов Михаил Олегович",
        "phone": "+7(926)697-15-41",
        "shift": "Ночная смена (20:00-08:00)",
        "start_date": datetime(2025, 9, 19)
    },
    "day_1": {
        "name": "Калион Михаил Евдокимович", 
        "phone": "+7(977)675-19-67",
        "shift": "Дневная смена (08:00-20:00)",
        "start_date": datetime(2025, 9, 19)
    },
    "night_2": {
        "name": "Фокин Василий Михайлович",
        "phone": "+7(967)085-48-15",
        "shift": "Ночная смена (20:00-08:00)", 
        "start_date": datetime(2025, 9, 21)
    },
    "day_2": {
        "name": "Алексеенко Алексей Алексеевич",
        "phone": "+7(926)040-34-69",
        "phone_extra": "+7(916)234-84-04",
        "shift": "Дневная смена (08:00-20:00)",
        "start_date": datetime(2025, 9, 21)
    }
}

def calculate_current_mechanic():
    now = datetime.now()
    current_time = now.time()
    
    if current_time >= datetime.strptime("08:00", "%H:%M").time() and current_time < datetime.strptime("20:00", "%H:%M").time():
        current_shift = "day"
        shift_start = datetime(now.year, now.month, now.day, 8, 0)
    else:
        current_shift = "night"
        if current_time < datetime.strptime("08:00", "%H:%M").time():
            shift_start = datetime(now.year, now.month, now.day, 20, 0) - timedelta(days=1)
        else:
            shift_start = datetime(now.year, now.month, now.day, 20, 0)
    
    base_date = datetime(2025, 9, 19)
    days_since_start = (shift_start - base_date).days
    cycle_day = days_since_start % 4
    
    if current_shift == "day":
        if cycle_day in [0, 1]:
            return MECHANICS_SCHEDULE["day_1"]
        else:
            return MECHANICS_SCHEDULE["day_2"]
    else:
        if cycle_day in [0, 1]:
            return MECHANICS_SCHEDULE["night_1"]
        else:
            return MECHANICS_SCHEDULE["night_2"]

def setup_mechanics_handlers(bot):
    @bot.message_handler(func=lambda m: m.text == '🔧 Текущий механик')
    def handle_current_mechanic(message):
        user_id = message.from_user.id
        save_user_message(user_id, message.message_id, message.chat.id)
        
        try:
            mechanic = calculate_current_mechanic()
            
            response = f"""🔧 ТЕКУЩИЙ МЕХАНИК

——— 👨‍🔧 СЕЙЧАС РАБОТАЕТ ———

👤 {mechanic['name']}
📞 {mechanic['phone']}"""

            if 'phone_extra' in mechanic:
                response += f"\n📞 {mechanic['phone_extra']}"
            
            response += f"\n⏰ {mechanic['shift']}"
            
            response += """

——— ⚠️ ВАЖНАЯ ИНФОРМАЦИЯ ———

• График работы: 2/2
• Смены: дневная (08:00-20:00), ночная (20:00-08:00)
• 4 механика в ротации

‼️ ВНИМАНИЕ: Данные предоставляются по штатному расписанию.
   Не учитываются:
   • Отпуска
   • Больничные листы  
   • Внеплановые замены
   • Командировки

💡 Для уточнения информации звоните на общий номер:
   📞 +7(495)950-40-00 доб. 17058"""

            send_message_with_cleanup(
                bot, user_id, message.chat.id,
                response,
                main_keyboard(user_id),
                log_action="current_mechanic"
            )
            
        except Exception as e:
            print(f"❌ Ошибка определения механика: {e}")
            send_message_with_cleanup(
                bot, user_id, message.chat.id,
                "❌ Не удалось определить текущего механика.\nПопробуйте позже.",
                main_keyboard(user_id),
                log_action="current_mechanic"
            )