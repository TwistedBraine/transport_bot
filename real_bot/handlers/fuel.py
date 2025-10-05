# -*- coding: utf-8 -*-
import telebot
from keyboards import main_keyboard
from utils import send_message_with_cleanup, save_user_message

TANK_CAPACITY = 68  # литров

def calculate_fuel_liters(percentage):
    try:
        percentage = float(percentage)
        if percentage < 0 or percentage > 100:
            return None, "❌ Процент должен быть от 0 до 100"
        
        liters = (percentage / 100) * TANK_CAPACITY
        return round(liters, 1), None
    except ValueError:
        return None, "❌ Введите число"

def setup_fuel_handlers(bot):
    @bot.message_handler(func=lambda m: m.text == '⛽ Расчет топлива')
    def handle_fuel_calc(message):
        user_id = message.from_user.id
        save_user_message(user_id, message.message_id, message.chat.id)
        
        response = f"""⛽ РАСЧЕТ ТОПЛИВА

📊 Информация:
• Полный бак: {TANK_CAPACITY} литров
• 100% = {TANK_CAPACITY} литров
• 50% = {TANK_CAPACITY/2} литров  
• 25% = {TANK_CAPACITY/4} литров

💡 Как пользоваться:
Введите остаток топлива в процентах (от 0 до 100)

Примеры:
• 50 - для 50%
• 25.5 - для 25.5%
• 100 - для полного бака

⬇️ Введите процент остатка топлива:"""

        send_message_with_cleanup(
            bot, user_id, message.chat.id,
            response,
            main_keyboard(user_id),
            log_action="fuel_calc"
        )
        bot.register_next_step_handler(message, process_fuel_percentage)
    
    def process_fuel_percentage(message):
        user_id = message.from_user.id
        save_user_message(user_id, message.message_id, message.chat.id)
        
        menu_buttons = ['🔍 Поиск водителей', '📞 Телефоны', '🚌 Маршруты', 
                       '🏥 Профосмотр', '🏢 Филиалы', '🌤️ Погода', 
                       '🔧 Текущий механик', '⛽ Расчет топлива', '📊 Статистика']
        
        if message.text in menu_buttons:
            return
        
        percentage = message.text.strip()
        liters, error = calculate_fuel_liters(percentage)
        
        if error:
            response = f"""❌ Ошибка ввода

{error}

💡 Правильный формат:
• Целое число: 50
• Дробное число: 25.5
• Диапазон: от 0 до 100

⬇️ Попробуйте еще раз:"""
            
            send_message_with_cleanup(
                bot, user_id, message.chat.id,
                response,
                main_keyboard(user_id),
                log_action="fuel_calc"
            )
            bot.register_next_step_handler(message, process_fuel_percentage)
        else:
            if liters == 0:
                fuel_emoji = "🪫"
            elif liters < TANK_CAPACITY * 0.25:
                fuel_emoji = "🟡"
            elif liters < TANK_CAPACITY * 0.5:
                fuel_emoji = "🟠"
            elif liters < TANK_CAPACITY * 0.75:
                fuel_emoji = "🟢"
            else:
                fuel_emoji = "✅"
            
            response = f"""⛽ РЕЗУЛЬТАТ РАСЧЕТА

{fuel_emoji} {percentage}% остатка топлива = {liters} литров

📊 Детали:
• Процент: {percentage}%
• Литры: {liters} л
• Полный бак: {TANK_CAPACITY} л

💡 Полезно знать:
• 100% = {TANK_CAPACITY} л
• 50% = {TANK_CAPACITY/2} л
• 25% = {TANK_CAPACITY/4} л

🔄 Новый расчет: нажмите «⛽ Расчет топлива»"""

            send_message_with_cleanup(
                bot, user_id, message.chat.id,
                response,
                main_keyboard(user_id),
                log_action="fuel_calc"
            )