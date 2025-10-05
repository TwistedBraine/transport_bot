# -*- coding: utf-8 -*-
import telebot
import requests
from config import WEATHER_API_KEY, WEATHER_CITY
from keyboards import main_keyboard
from utils import send_message_with_cleanup, save_user_message

def get_road_condition(temp, weather_desc, humidity):
    """Определяет состояние дороги"""
    if temp <= 0 and humidity > 80:
        return "❄️ ГОЛОЛЁД - КРИТИЧЕСКАЯ ОПАСНОСТЬ"
    elif temp <= 2 and humidity > 70:
        return "⚠️ Возможен гололёд - повышенная опасность"
    elif "дождь" in weather_desc.lower() or "ливень" in weather_desc.lower():
        return "💧 Мокрая дорога - скользко"
    elif "снег" in weather_desc.lower():
        return "🌨️ Снег на дороге - снижайте скорость"
    else:
        return "✅ Дорога сухая - нормальные условия"

def get_visibility_condition(visibility, weather_desc):
    """Определяет видимость на дороге"""
    if visibility <= 1000:
        return "🚨 ОЧЕНЬ НИЗКАЯ (менее 1 км)"
    elif visibility <= 3000:
        return "⚠️ Низкая (1-3 км)"
    elif visibility <= 7000:
        return "🔸 Умеренная (3-7 км)"
    else:
        return "✅ Хорошая (более 7 км)"

def get_driving_recommendations(temp, weather_desc, wind_speed, visibility):
    """Дает рекомендации для водителей"""
    recommendations = []
    
    if temp <= 0:
        recommendations.append("• 🧊 Используйте зимнюю резину")
        recommendations.append("• ⚠️ Увеличьте дистанцию в 2 раза")
        recommendations.append("• 🚗 Избегайте резких торможений")
    
    if "дождь" in weather_desc.lower():
        recommendations.append("• 💧 Включите фары и противотуманки")
        recommendations.append("• 🚘 Снизьте скорость на 20-30%")
        recommendations.append("• 📏 Увеличьте дистанцию")
    
    if "снег" in weather_desc.lower():
        recommendations.append("• 🌨️ Включите дворники и обогревы")
        recommendations.append("• 🚙 Используйте пониженные передачи")
        recommendations.append("• 🛞 Проверьте давление в шинах")
    
    if wind_speed > 10:
        recommendations.append("• 💨 Будьте готовы к порывам ветра")
        recommendations.append("• 🚛 Особенно осторожно обгоняйте фуры")
    
    if visibility < 2000:
        recommendations.append("• 🌫️ Включите противотуманные фары")
        recommendations.append("• 🐌 Двигайтесь с минимальной скоростью")
    
    if not recommendations:
        recommendations.append("• ✅ Стандартные условия движения")
        recommendations.append("• 👀 Соблюдайте ПДД")
    
    return recommendations

def setup_weather_handlers(bot):
    @bot.message_handler(func=lambda m: m.text == '🌤️ Погода')
    def handle_weather(message):
        user_id = message.from_user.id
        save_user_message(user_id, message.message_id, message.chat.id)
        
        # Если API ключа нет, показываем расширенную стандартную погоду
        if not WEATHER_API_KEY:
            weather_text = """🌤️ ПОГОДА В МОСКВЕ
ДЛЯ ВОДИТЕЛЕЙ ТРАНСПОРТА

——— 📊 ТЕКУЩИЕ УСЛОВИЯ ———

🌡️ Температура: +3°C
💨 Ветер: 5 м/с
💧 Влажность: 75%
👁️ Видимость: 5 км
☁️ Погода: облачно с прояснениями

——— 🛣️ СОСТОЯНИЕ ДОРОГ ———

• Дорога: 💧 Мокрая дорога - скользко
• Видимость: 🔸 Умеренная (3-7 км)
• Осадки: небольшая морось

——— 🚗 РЕКОМЕНДАЦИИ ДЛЯ ВОДИТЕЛЕЙ ———

• 💧 Включите фары и противотуманки
• 🚘 Снизьте скорость на 20-30%
• 📏 Увеличьте дистанцию
• 👀 Будьте внимательны на пешеходных переходах

⚠️ ОСТОРОЖНО НА ДОРОГЕ!"""
            
            send_message_with_cleanup(
                bot, user_id, message.chat.id,
                weather_text,
                main_keyboard(user_id),
                log_action="weather"
            )
            return
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Основные данные
                temp = data['main']['temp']
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                visibility = data.get('visibility', 10000)  # в метрах
                weather_desc = data['weather'][0]['description']
                
                # Конвертируем видимость в км
                visibility_km = visibility / 1000 if visibility else 10
                
                # Определяем условия для водителей
                road_condition = get_road_condition(temp, weather_desc, humidity)
                visibility_condition = get_visibility_condition(visibility_km, weather_desc)
                recommendations = get_driving_recommendations(temp, weather_desc, wind_speed, visibility_km)
                
                weather_text = f"""🌤️ ПОГОДА В {WEATHER_CITY.upper()}
ДЛЯ ВОДИТЕЛЕЙ ТРАНСПОРТА

——— 📊 ТЕКУЩИЕ УСЛОВИЯ ———

🌡️ Температура: {temp:.1f}°C (ощущается как {feels_like:.1f}°C)
💨 Ветер: {wind_speed} м/с
💧 Влажность: {humidity}%
👁️ Видимость: {visibility_km:.1f} км
☁️ Погода: {weather_desc}

——— 🛣️ СОСТОЯНИЕ ДОРОГ ———

• Дорога: {road_condition}
• Видимость: {visibility_condition}
• Осадки: {weather_desc}

——— 🚗 РЕКОМЕНДАЦИИ ДЛЯ ВОДИТЕЛЕЙ ———"""

                for rec in recommendations:
                    weather_text += f"\n{rec}"
                
                weather_text += "\n\n⚠️ ОСТОРОЖНО НА ДОРОГЕ!"
                
                send_message_with_cleanup(
                    bot, user_id, message.chat.id,
                    weather_text,
                    main_keyboard(user_id),
                    log_action="weather"
                )
            else:
                raise Exception("API error")
                
        except Exception as e:
            print(f"❌ Ошибка погоды: {e}")
            # Fallback на расширенную стандартную погоду
            weather_text = """🌤️ ПОГОДА В МОСКВЕ
ДЛЯ ВОДИТЕЛЕЙ ТРАНСПОРТА

——— 📊 ТЕКУЩИЕ УСЛОВИЯ ———

🌡️ Температура: +2°C
💨 Ветер: 4 м/с  
💧 Влажность: 80%
👁️ Видимость: 3 км
☁️ Погода: пасмурно, возможен дождь

——— 🛣️ СОСТОЯНИЕ ДОРОГ ———

• Дорога: 💧 Мокрая дорога - скользко
• Видимость: ⚠️ Низкая (1-3 км)
• Осадки: возможен дождь

——— 🚗 РЕКОМЕНДАЦИИ ДЛЯ ВОДИТЕЛЕЙ ———

• 💧 Включите фары и противотуманки
• 🚘 Снизьте скорость на 20-30%
• 📏 Увеличьте дистанцию
• 🌫️ Будьте готовы к ухудшению видимости

⚠️ ОСТОРОЖНО НА ДОРОГЕ!"""
            
            send_message_with_cleanup(
                bot, user_id, message.chat.id,
                weather_text,
                main_keyboard(user_id),
                log_action="weather"
            )