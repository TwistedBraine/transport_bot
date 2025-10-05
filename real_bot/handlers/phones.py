# -*- coding: utf-8 -*-
import telebot
from keyboards import phones_keyboard, main_keyboard
from utils import send_message_with_cleanup, save_user_message

def setup_phones_handlers(bot):  # ← ОТКРЫВАЕМ ФУНКЦИЮ
    
    @bot.message_handler(func=lambda m: m.text == '📞 Телефоны')
    def handle_phones(message):
        user_id = message.from_user.id
        save_user_message(user_id, message.message_id, message.chat.id)
        
        send_message_with_cleanup(
            bot, user_id, message.chat.id,
            "📞 Выберите раздел:",
            phones_keyboard(),
            log_action="phones_menu"
        )
    
    @bot.message_handler(func=lambda m: m.text == '📞 Телефоны парка')
    def handle_park_phones(message):
        user_id = message.from_user.id
        save_user_message(user_id, message.message_id, message.chat.id)
        
        text = """🏢 ТЕЛЕФОНЫ ПАРКА

📞 Главный номер: +7(495)950-40-00

Диспетчерские:
• 16900, 6752 - Диспетчер выпуска
• 17063 - ЦУП
• 14154 - Расчетная часть 6АЭД

Мобильные:
• Диспетчер выпуска: +7(919)784-00-70
• Диспетчер ЦУП: +7(985)169-90-15
• Начальник смены: +7(985)169-90-14
• АСДУ: +7(985)169-90-13
• КАМАЗ: +7(985)400-36-02

Ситуационный центр:
+7(495)951-20-23

⏰ Круглосуточно"""
        
        send_message_with_cleanup(
            bot, user_id, message.chat.id,
            text,
            main_keyboard(user_id),
            log_action="phones_park"
        )
    
    @bot.message_handler(func=lambda m: m.text == '👔 Телефоны руководства')
    def handle_management_phones(message):
        user_id = message.from_user.id
        save_user_message(user_id, message.message_id, message.chat.id)
        
        text = """👔 РУКОВОДСТВО КОЛОННЫ

Начальник колонны:
• Величкин Сергей Дмитриевич
• +7(999)991-24-21

Зам. по эксплуатации:
• Карпов Виктор Сергеевич
• +7(985)834-97-57

Зам. по технической части:
• Яковлев Алексей Вячеславович
• +7(903)523-38-21

Старший механик:
• Татарников Андрей Анатольевич
• +7(925)874-09-11

Ведущий инженер:
• Федотова Тамара Арменовна
• +7(977)340-72-13

Механик колонны:
• +7(495)950-40-00 доб. 17058

⏰ Пн-Пт: 08:00-17:00"""
        
        send_message_with_cleanup(
            bot, user_id, message.chat.id,
            text,
            main_keyboard(user_id),
            log_action="phones_management"
        )
    
    @bot.message_handler(func=lambda m: m.text == '🛰️ Телефоны ГЛОНАСС')
    def handle_glonass_phones(message):
        user_id = message.from_user.id
        save_user_message(user_id, message.message_id, message.chat.id)
        
        text = """🛰️ ТЕЛЕФОНЫ ГЛОНАСС

📞 Главный номер: +7(495)787-43-30

——— 📞 ВСЕ ОПЕРАТОРЫ ———

<b>4254</b> - 72
<b>4264</b> - 167, 563, 76  
<b>4265</b> - 76, <b>149</b>
<b>4275</b> - <b>H6</b>, <b>E59</b>, <b>353</b>
<b>4276</b> - 447, 763
<b>4277</b> - T36, 170, <b>604</b>
<b>4278</b> - 154
<b>4263</b> - H9, M44K, 136, 586
<b>4279</b> - M54

<b>4121</b> - Старший диспетчер

⏰ Круглосуточно"""

        send_message_with_cleanup(
            bot, user_id, message.chat.id,
            text,
            main_keyboard(user_id),
            log_action="phones_glonass",
            parse_mode="HTML"

        )

# ← ВОТ ТУТ ДОЛЖНА БЫТЬ ЗАКРЫВАЮЩАЯ СКОБКА! ↓ # ← ДОБАВЬ ЭТУ СТРОКУ!