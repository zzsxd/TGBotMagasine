#####################################
#            Created by             #
#               zzsxd               #
#               SBR                 #
#####################################
config_name = 'secrets.json'
#####################################

import os
import telebot
import platform
from datetime import datetime
import threading
from threading import Lock
import time
from config_parser import ConfigParser
from frontend import Bot_inline_btns
from backend import TempUserData, DbAct
from db import DB



def main():
    @bot.message_handler(commands=['start', 'admin'])
    def start_msg(message):
        name_user = message.from_user.first_name
        user_id = message.from_user.id
        buttons = Bot_inline_btns()
        command = message.text.replace('/', '')
        db_actions.add_user(user_id, message.from_user.first_name, message.from_user.last_name,
                            f'@{message.from_user.username}')
        if command == 'start':
            bot.send_message(message.chat.id, 'start message',
                             reply_markup=buttons.start_btns(), parse_mode="HTML")
        elif db_actions.user_is_admin(user_id):
            if command == 'admin':
                bot.send_message(message.chat.id, f'{message.from_user.first_name}, вы успешно вошли в Админ-Панель ✅',
                                 reply_markup=buttons.admin_btns())

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        buttons = Bot_inline_btns()
        # пользовательские команды
        if call.data == 'assortiment':
            bot.send_message(call.message.chat.id, 'Наш ассортимент товаров: ', reply_markup=buttons.assortiment_btns())
        elif call.data == 'cart':
            bot.send_message(call.message.chat.id, 'Корзина')
        elif call.data == 'bonus':
            bot.send_message(call.message.chat.id, 'Наши скидки и акции', reply_markup=buttons.bonus_btns())
        elif call.data == 'reviews':
            bot.send_message(call.message.chat.id, 'Отзывы', reply_markup=buttons.reviews_btns())
        elif call.data == 'faq':
            bot.send_message(call.message.chat.id, 'Ответы на все вопросы', reply_markup=buttons.faq_btns())
        elif call.data == ''
        # команды админа
        elif call.data == 'export':
            db_actions.db_export_xlsx()
            bot.send_document(call.message.chat.id, open(config.get_config()['xlsx_path'], 'rb'))
            os.remove(config.get_config()['xlsx_path'])
        elif call.data == 'addtovar':
            pass #добавление товара
        elif call.data == 'changetovar':
            pass #изменение товара
        elif call.data == 'newsletter':
            pass #рассылка всем пользователям
    bot.polling(none_stop=True)


if '__main__' == __name__:
    os_type = platform.system()
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(f'{work_dir}/{config_name}', os_type)
    temp_user_data = TempUserData()
    db = DB(config.get_config()['db_file_name'], Lock())
    db_actions = DbAct(db, config, config.get_config()['xlsx_path'])
    bot = telebot.TeleBot(config.get_config()['tg_api'])
    main()

