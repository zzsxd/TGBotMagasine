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
        user_id = call.message.chat.id
        buttons = Bot_inline_btns()
        if db_actions.user_is_existed(user_id):
            print(1)
            code = temp_user_data.temp_data(user_id)[user_id][0]
            if call.data == 'assortiment':
                temp_user_data.temp_data(user_id)[user_id][0] = 10
                categories = db_actions.get_categories()
                bot.send_message(user_id, 'Выберите категорию: ',
                                 reply_markup=buttons.assortiment_btns(categories))
            elif call.data == 'cart':
                s = ''
                all_cost = 0
                shipping_cart = db_actions.get_shipping_cart_by_user_id(user_id)
                for i in range(len(shipping_cart)):
                    product = db_actions.get_product_by_id(shipping_cart[i])
                    all_cost += int(product[1])
                    s += f'{i+1}. {product[0]} - {product[1]}\n'
                bot.send_message(user_id, f'Ваша корзина:\n{s}\n\nобщая цена товаров: {all_cost}', reply_markup=buttons.pay_shipping_cart())
            elif call.data == 'bonus':
                bot.send_message(call.message.chat.id, 'Наши скидки и акции', reply_markup=buttons.bonus_btns())
            elif call.data == 'pay_shipping_cart':
                bot.send_message(call.message.chat.id, 'Кода нет - тимлид уснул')
            elif call.data == 'reviews':
                bot.send_message(call.message.chat.id, 'Отзывы', reply_markup=buttons.reviews_btns())
            elif call.data == 'faq':
                bot.send_message(call.message.chat.id, 'Ответы на все вопросы', reply_markup=buttons.faq_btns())
            elif call.data[:8] == 'category' and code == 10:
                temp_user_data.temp_data(user_id)[user_id][0] = None
                products = db_actions.products_by_id_category(call.data[8:])
                for product in products:
                    bot.send_photo(chat_id=user_id, caption=f'{product[1]}\n\n{product[2]}', photo=product[3],
                                   reply_markup=buttons.add_product_to_shipping_cart(product[0]))
            elif call.data[:8] == 'addtobuy':
                if db_actions.update_shipping_cart(user_id, call.data[8:]):
                    bot.answer_callback_query(call.id, "Товар добавлен в корзину", show_alert=True)
                else:
                    bot.answer_callback_query(call.id, "Товар уже в корзине", show_alert=True)
            if db_actions.user_is_admin(user_id):
                if call.data == 'export':
                    db_actions.db_export_xlsx()
                    bot.send_document(call.message.chat.id, open(config.get_config()['xlsx_path'], 'rb'))
                    os.remove(config.get_config()['xlsx_path'])
                elif call.data[:8] == 'category' and code == 3:
                    temp_user_data.temp_data(user_id)[user_id][1][3] = call.data[8:]
                    db_actions.add_product(temp_user_data.temp_data(user_id)[user_id][1])
                    temp_user_data.temp_data(user_id)[user_id][0] = None
                    bot.send_message(user_id, 'Товар успешно добавлен!')
                elif call.data[:8] == 'category' and code == 5:
                    db_actions.del_categories(call.data[8:])
                    temp_user_data.temp_data(user_id)[user_id][0] = None
                    bot.send_message(user_id, 'Категория удалена успешно!')
                elif call.data[:8] == 'category' and code == 9:
                    db_actions.update_product('categori_id', call.data[8:], temp_user_data.temp_data(user_id)[user_id][2])
                    temp_user_data.temp_data(user_id)[user_id][0] = None
                    bot.send_message(user_id, 'Товар успешно обновлён!')
                elif call.data == 'delcategory':
                    temp_user_data.temp_data(user_id)[user_id][0] = 5
                    categories = db_actions.get_categories()
                    bot.send_message(user_id, 'Выберите категорию для удаления',
                                     reply_markup=buttons.categories_btns(categories))
                elif call.data[:22] == 'finally_change_product':
                    match call.data[22]:
                        case '1':
                            temp_user_data.temp_data(user_id)[user_id][0] = 6
                            bot.send_message(user_id, 'Введите новое название')
                        case '2':
                            temp_user_data.temp_data(user_id)[user_id][0] = 7
                            bot.send_message(user_id, 'Введите новое описание')
                        case '3':
                            temp_user_data.temp_data(user_id)[user_id][0] = 8
                            bot.send_message(user_id, 'Отправьте новую обложку')
                        case '4':
                            categories = db_actions.get_categories()
                            temp_user_data.temp_data(user_id)[user_id][0] = 9
                            bot.send_message(user_id, 'Выберите новую категорию', reply_markup=buttons.categories_btns(categories))
                        case '5':
                            temp_user_data.temp_data(user_id)[user_id][0] = 10
                            bot.send_message(user_id, 'Введите новую цену')
                elif call.data[:14] == 'change_product':
                    temp_user_data.temp_data(user_id)[user_id][2] = call.data[14:]
                    bot.send_message(user_id, 'Что вы хотите изменить?',
                                     reply_markup=buttons.change_peoduct_btns())
                elif call.data == 'addtovar':
                    temp_user_data.temp_data(user_id)[user_id][0] = 0
                    bot.send_message(user_id, 'Введите название товара')
                elif call.data == 'addcategory':
                    temp_user_data.temp_data(user_id)[user_id][0] = 4
                    bot.send_message(user_id, 'Введите название категории')
                elif call.data == 'changetovar':
                    products = db_actions.get_products_preview()
                    bot.send_message(user_id, 'Выберите товар',
                                     reply_markup=buttons.product_btns(products))
                elif call.data == 'newsletter':
                    pass #рассылка всем пользователям

    @bot.message_handler(content_types=['text', 'photo'])
    def text_message(message):
        photo = message.photo
        user_input = message.text
        user_id = message.chat.id
        buttons = Bot_inline_btns()
        if db_actions.user_is_existed(user_id):
            code = temp_user_data.temp_data(user_id)[user_id][0]
            match code:
                case 0:
                    if user_input is not None:
                        temp_user_data.temp_data(user_id)[user_id][1][0] = user_input
                        temp_user_data.temp_data(user_id)[user_id][0] = 1
                        bot.send_message(user_id, 'Отправьте фото товара')
                    else:
                        bot.send_message(user_id, 'Это не текст!')
                case 1:
                    if photo is not None:
                        photo_id = photo[-1].file_id
                        photo_file = bot.get_file(photo_id)
                        photo_bytes = bot.download_file(photo_file.file_path)
                        temp_user_data.temp_data(user_id)[user_id][1][1] = photo_bytes
                        temp_user_data.temp_data(user_id)[user_id][0] = 11
                        bot.send_message(user_id, 'Отправьте цену товара')
                    else:
                        bot.send_message(user_id, 'Это не фото!')
                case 2:
                    if user_input is not None:
                        temp_user_data.temp_data(user_id)[user_id][1][2] = user_input
                        temp_user_data.temp_data(user_id)[user_id][0] = 3
                        categories = db_actions.get_categories()
                        bot.send_message(user_id, 'Выберите категорию для товара', reply_markup=buttons.categories_btns(categories))
                    else:
                        bot.send_message(user_id, 'Это не текст!')
                case 4:
                    if user_input is not None:
                        db_actions.add_category(user_input)
                        temp_user_data.temp_data(user_id)[user_id][0] = None
                        bot.send_message(user_id, 'Категория успешно добавлена!')
                    else:
                        bot.send_message(user_id, 'Это не текст!')
                case 6:
                    if user_input is not None:
                        db_actions.update_product('name', user_input, temp_user_data.temp_data(user_id)[user_id][2])
                        temp_user_data.temp_data(user_id)[user_id][0] = None
                        bot.send_message(user_id, 'Товар успешно обновлён!')
                    else:
                        bot.send_message(user_id, 'Это не текст!')
                case 7:
                    if user_input is not None:
                        db_actions.update_product('description', user_input, temp_user_data.temp_data(user_id)[user_id][2])
                        temp_user_data.temp_data(user_id)[user_id][0] = None
                        bot.send_message(user_id, 'Товар успешно обновлён!')
                    else:
                        bot.send_message(user_id, 'Это не текст!')
                case 8:
                    if photo is not None:
                        photo_id = photo[-1].file_id
                        photo_file = bot.get_file(photo_id)
                        photo_bytes = bot.download_file(photo_file.file_path)
                        db_actions.update_product('photo', photo_bytes, temp_user_data.temp_data(user_id)[user_id][2])
                        temp_user_data.temp_data(user_id)[user_id][0] = None
                        bot.send_message(user_id, 'Товар успешно обновлён!')
                    else:
                        bot.send_message(user_id, 'Это не фото!')
                case 10:
                    if user_input is not None:
                        db_actions.update_product('price', user_input,
                                                  temp_user_data.temp_data(user_id)[user_id][2])
                        temp_user_data.temp_data(user_id)[user_id][0] = None
                        bot.send_message(user_id, 'Товар успешно обновлён!')
                    else:
                        bot.send_message(user_id, 'Это не текст!')
                case 11:
                    if user_input is not None:
                        try:
                            temp_user_data.temp_data(user_id)[user_id][1][4] = int(user_input)
                            temp_user_data.temp_data(user_id)[user_id][0] = 2
                            bot.send_message(user_id, 'Отправьте описание товара')
                        except:
                            bot.send_message(user_id, 'Это не число!')
                    else:
                        bot.send_message(user_id, 'Это не текст!')

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

