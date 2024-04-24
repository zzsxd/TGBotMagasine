#####################################
#            Created by             #
#               zzsxd               #
#               SBR                 #
#####################################
config_name = 'secrets.json'
#####################################

import os
import telebot
from telebot import types
import platform
from threading import Lock
from config_parser import ConfigParser
from frontend import Bot_inline_btns
from backend import TempUserData, DbAct
from db import DB


def start_message(user_id):
    buttons = Bot_inline_btns()
    image_path = 'first.png'
    with open(image_path, 'rb') as photo:
        bot.send_photo(chat_id=user_id, caption='Wassup и добро пожаловать в Wakcup Shop!🫗\n\n'
                              'Я помогу тебе оформить заказ и ответить на вопросы.', photo=photo,
                     reply_markup=buttons.start_btns())


def proccess_redirect(user_id):
    buttons = Bot_inline_btns()
    product = db_actions.products_by_id_category(temp_user_data.temp_data(user_id)[user_id][5][1],
                                                 temp_user_data.temp_data(user_id)[user_id][5][2][temp_user_data.temp_data(user_id)[user_id][5][0]])
    if len(product) != 0:
        product = product[0]
        bot.send_photo(chat_id=user_id, caption=f'Название: {product[0]}\n\nЦена: {product[3]}₽\n\nОписание: {product[1]}', photo=product[2],
                       reply_markup=buttons.add_product_to_shipping_cart(temp_user_data.temp_data(user_id)[user_id][5][2][
                                                                             temp_user_data.temp_data(user_id)[user_id][5][
                                                                                 0]]))
    else:
        bot.send_message(user_id, 'Категория пуста')


def show_product(user_id, direction):
    if direction == '1':
        if temp_user_data.temp_data(user_id)[user_id][5][0] + 1 < len(temp_user_data.temp_data(user_id)[user_id][5][2]):
            temp_user_data.temp_data(user_id)[user_id][5][0] += 1
            proccess_redirect(user_id)
    else:
        if temp_user_data.temp_data(user_id)[user_id][5][0] - 1 >= 0:
            temp_user_data.temp_data(user_id)[user_id][5][0] -= 1
            proccess_redirect(user_id)


def main():
    @bot.message_handler(commands=['start', 'admin'])
    def start_msg(message):
        name_user = message.from_user.first_name
        user_id = message.from_user.id
        buttons = Bot_inline_btns()
        image_path = 'first'
        command = message.text.replace('/', '')
        if db_actions.user_is_existed(user_id):
            if command == 'start':
                start_message(user_id)
            elif db_actions.user_is_admin(user_id):
                if command == 'admin':
                    bot.send_message(message.chat.id,
                                     f'{message.from_user.first_name}, вы успешно вошли в Админ-Панель ✅',
                                     reply_markup=buttons.admin_btns())
        else:
            start_message(user_id)
        db_actions.add_user(user_id)

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        image_path1 = 'thx.png'
        image_path2 = 'scam.png'
        image_path3 = 'answer.png'
        user_id = call.message.chat.id
        buttons = Bot_inline_btns()
        if db_actions.user_is_existed(user_id):
            code = temp_user_data.temp_data(user_id)[user_id][0]
            if call.data == 'assortiment':
                temp_user_data.temp_data(user_id)[user_id][0] = 10
                categories = db_actions.get_categories()
                bot.send_message(user_id, 'Выберите категорию: ',
                                 reply_markup=buttons.assortiment_btns(categories))
            elif call.data == 'cart':
                s = ''
                all_cost = 0
                counter = 0
                shipping_cart = db_actions.get_shipping_cart_by_user_id(user_id)
                for i, g in shipping_cart.items():
                    counter += 1
                    product = db_actions.get_product_by_id(i)
                    all_cost += int(product[1]) * int(g)
                    s += f'{counter}. {product[0]} - {int(product[1]) * int(g)} ({g}X)\n'
                bot.send_message(user_id, f'Ваша корзина 🛒\n{s}\n\nОбщая цена товаров: {all_cost}',
                                 reply_markup=buttons.pay_shipping_cart())
            elif call.data == 'change_shopping_cart':
                data = list()
                shipping_cart = db_actions.get_shipping_cart_by_user_id(user_id)
                for i in shipping_cart.keys():
                    name = db_actions.get_product_by_id(i)[0]
                    data.append([name, i])
                bot.send_message(user_id, 'Выберите товар в корзине для изменения', reply_markup=buttons.shipping_products_change_btns(data))
            elif call.data[:18] == 'changeproduct_cart':
                temp_user_data.temp_data(user_id)[user_id][6] = call.data[18:]
                bot.send_message(user_id, 'Выберите действие', reply_markup=buttons.shipping_products_delete_btns())
            elif call.data[:21] == 'delete_shopping_cart':
                if db_actions.delete_shipping_cart(user_id, temp_user_data.temp_data(user_id)[user_id][6]):
                    bot.send_message(user_id, 'Действие успешно завершено', reply_markup=buttons.back_to_cart_btns())
                else:
                    bot.send_message(user_id, 'Товар отсутствует в вашей корзине!', reply_markup=buttons.back_to_cart_btns())
            elif call.data[:21] == 'quanity_shopping_cart':
                temp_user_data.temp_data(user_id)[user_id][0] = 20
                bot.send_message(user_id, 'Введите новое количество')
            elif call.data == 'bonus':
                bot.send_message(call.message.chat.id, 'Наши скидки и акции', reply_markup=buttons.bonus_btns())
            elif call.data == 'pay_shipping_cart':
                s = ''
                all_cost = 0
                counter = 0
                shipping_cart = db_actions.get_shipping_cart_by_user_id(user_id)
                for i, g in shipping_cart.items():
                    counter += 1
                    product = db_actions.get_product_by_id(i)
                    all_cost += int(product[1]) * int(g)
                    s += f'{counter}. {product[0]} - {product[1] * int(g)} ({g}X)\n'
                bot.send_invoice(
                    chat_id=user_id,
                    title='Покупка товаров',
                    description='от бота Wakcup Seller',
                    invoice_payload=s,
                    provider_token='390540012:LIVE:49518',
                    start_parameter='asdasda',
                    currency='RUB',
                    prices=[types.LabeledPrice("Товар", all_cost * 100)])
            elif call.data == 'reviews':
                with open(image_path2, 'rb') as photo:
                    bot.send_photo(chat_id=call.message.chat.id,
                                 caption='Мы работаем уже год, и за это время отправили тысячи посылок и собрали сотни отзывов, можешь их чекнуть!\n'
                                 'Так же, у нас работает правило: если мы не отправляем заказ в течение недели, мы дарим тебе сироп, кидаем его в посылку без доплат.', photo=photo, reply_markup=buttons.reviews_btns())
            elif call.data == 'faq':
                with open(image_path3, 'rb') as photo:
                    bot.send_photo(chat_id=call.message.chat.id, caption='Ответы на все вопросы', photo=photo, reply_markup=buttons.faq_btns())
            elif call.data == 'order':
                bot.send_message(call.message.chat.id, 'Оформление осуществляется через данного бота.\n\n'
                                                       '📲 Для этого зайди в: \n'
                                                       '<b>"Ассортимент и цены" -> выбери товары и добавь их в корзину -> перейди в корзину, и нажми "Купить", далее нужно указать свои данные для получения и провести оплату.</b>\n\n'
                                                       '💳 Оплата осуществляется за товар во время оформления, а за доставку при получении, примерную стоимость можете посмотреть по кнопке "<b>Доставка</b>".', reply_markup=buttons.backorder_btns(), parse_mode='HTML')
            elif call.data == 'delivery':
                bot.send_message(call.message.chat.id, '📦 Доставка осуществляется транспортной компанией <b>СДЭК</b> почти по всему миру до пункта выдачи (выбираете сами, там же ее и оплачиваете при получении).\n\n'
                                                       '❗️Получение <b>по паспорту</b> или <b>СДЭК id</b>. Есть возможность отправки почтой РФ, если так будет выгоднее для покупателя.\n\n'
                                                       '<b>Вот примерная стоимость доставки ( все зависит от заказа ) по городам:</b>\n'
                                                       '•Москва и МО - 370р. / 1-2 раб. дня\n'
                                                       '•СПБ - 398р. / 2-3 раб. дня\n'
                                                       '•Минск - 485р. / 4-5 раб. дней\n'
                                                       '•Новосибирск - 543р. / 3-5 раб. дней\n'
                                                       '•Екатеринбург - 415р. / 3-4 раб. дня\n'
                                                       '•Астрахань - 429р. / 3-5 раб. дней\n'
                                                       '•Ростов-на-Дону - 389р. / 3-4 раб. дня\n'
                                                       '•Красноярск - 575р. / 5-7раб. дней\n'
                                                       '•Казань - 389р. / 2-3 раб. дня\n'
                                                       '•Нижний Новгород - 389р. / 2-3 раб. дня\n'
                                                       '•Самара - 398р. / 3-4 раб. дня\n'
                                                       '•Краснодар -398р. / 3-4 раб. дня\n'
                                                       '•Пенза - 416р. / 2-3 раб. дня\n'
                                                       '•Иркутск - 655р. / 9-11 раб. дней\n'
                                                       '•Южно-Сахалинск - 719р. / 23-25 раб. дней\n'
                                                       '•Омск - 560р. / 4-6 раб. дней\n'
                                                       '•Ярославль - 389р. / 2-3 раб. дня\n'
                                                       '•Челябинск - 380р. / 3-4 раб. дня\n'
                                                       '•Сыктывкар - 414р. / 3-4 раб. дня\n\n'
                                                       '<i>- Если вашего города тут нет, но он находится рядом с одним из '
                                                       'вышеперечисленных, то цена и сроки доставки сильно не '
                                                       'изменятся, не надо писать по такому поводу менеджеру, '
                                                       'если только вам совсем принципиально.</i>', reply_markup=buttons.back_btns(), parse_mode='HTML')
            elif call.data == 'delivery1':
                bot.send_message(call.message.chat.id, '📦 Доставка осуществляется транспортной компанией <b>СДЭК</b> почти по всему миру до пункта выдачи (выбираете сами, там же ее и оплачиваете при получении).\n\n'
                                                       '❗️Получение <b>по паспорту</b> или <b>СДЭК id</b>. Есть возможность отправки почтой РФ, если так будет выгоднее для покупателя.\n\n'
                                                       '<b>Вот примерная стоимость доставки ( все зависит от заказа ) по городам:</b>\n'
                                                       '•Москва и МО - 370р. / 1-2 раб. дня\n'
                                                       '•СПБ - 398р. / 2-3 раб. дня\n'
                                                       '•Минск - 485р. / 4-5 раб. дней\n'
                                                       '•Новосибирск - 543р. / 3-5 раб. дней\n'
                                                       '•Екатеринбург - 415р. / 3-4 раб. дня\n'
                                                       '•Астрахань - 429р. / 3-5 раб. дней\n'
                                                       '•Ростов-на-Дону - 389р. / 3-4 раб. дня\n'
                                                       '•Красноярск - 575р. / 5-7раб. дней\n'
                                                       '•Казань - 389р. / 2-3 раб. дня\n'
                                                       '•Нижний Новгород - 389р. / 2-3 раб. дня\n'
                                                       '•Самара - 398р. / 3-4 раб. дня\n'
                                                       '•Краснодар -398р. / 3-4 раб. дня\n'
                                                       '•Пенза - 416р. / 2-3 раб. дня\n'
                                                       '•Иркутск - 655р. / 9-11 раб. дней\n'
                                                       '•Южно-Сахалинск - 719р. / 23-25 раб. дней\n'
                                                       '•Омск - 560р. / 4-6 раб. дней\n'
                                                       '•Ярославль - 389р. / 2-3 раб. дня\n'
                                                       '•Челябинск - 380р. / 3-4 раб. дня\n'
                                                       '•Сыктывкар - 414р. / 3-4 раб. дня\n\n'
                                                       '<i>- Если вашего города тут нет, но он находится рядом с одним из '
                                                       'вышеперечисленных, то цена и сроки доставки сильно не '
                                                       'изменятся, не надо писать по такому поводу менеджеру, '
                                                       'если только вам совсем принципиально.</i>', reply_markup=buttons.backkorzina_btns(), parse_mode='HTML')
            elif call.data == 'legal':
                bot.send_message(call.message.chat.id, 'Да, это абсолютно легально и безопасно, вас никто не примет на пункте выдачи.\n'
                                                       '🚫 В составе сиропа нет кодеина, прометазина и других запрещенных веществ, так что он абсолютно легален, эффект создает <b>мелатонин</b>, который успокаивает, вызывает сонливость, расслабляет и клонит в сон.\n'
                                                       ' - Есть еще элементы, которые придают вкус и запах похожий на оригинальный американский сироп, но эффект <b>не будет сильным</b>, т.к. мы не можем сделать легально сильный эффект.', reply_markup=buttons.back_btns(), parse_mode='HTML')
            elif call.data == 'sirop':
                bot.send_message(call.message.chat.id, 'Мы производим сироп для разбавления со спрайтом, чтобы получился напиток, похожий на лин, но <b>абсолютно легально</b>✅\n\n'
                                                       '🫗Чтобы получился готовый напиток, необходимо залить<b> 1/3 или 1/2 (от 100мл) в спрайт 0,5, взболтать, перелить все в дабл кап, добавить джолли ранчерс (на свое усмотрение), добавить лед.</b> Все, "линчик" готов.\n\n'
                                                       'В составе сиропа <b>нет кодеина, прометазина</b> и других запрещенных веществ, так что он абсолютно легален, эффект создает <b>мелатонин и экстракт валерьяны</b>, которые успокаивают, вызывают сонливость и расслабляют😵‍💫\n\n'
                                                       '🧬Есть еще элементы, которые придают вкус и запах похожий на оригинальный американский сироп, но эффект <b>не будет сильным, тк мы не можем сделать легально сильный эффект.</b>', reply_markup=buttons.back_btns(), parse_mode='HTML')
            elif call.data == 'notdelivery':
                bot.send_message(call.message.chat.id, '📜У нас работает правило:\n\n'
                                                       'Если мы не отправляем заказ в течение недели, мы дарим тебе сироп, кидаем его в посылку без доплат.\n\n'
                                                       'Если ты ждешь больше недели, то обратись к нашему менеджеру по кнопке ниже, и мы закинем тебе доп сироп👇🏻', reply_markup=buttons.backdev_btns())
            elif call.data == 'guarantees':
                bot.send_message(call.message.chat.id, '✅Мы работаем уже год, и за это время отправили тысячи посылок и собрали сотни отзывов, можешь их чекнуть!\n\n'
                                                       '📜Так же, у нас работает правило: если мы не отправляем заказ в течение недели, мы дарим тебе сироп, кидаем его в посылку без доплат.',
                                 reply_markup=buttons.guarantees_btns())
            elif call.data == 'taketenprocents':
                bot.send_message(call.message.chat.id, 'Ты знаешь кентов, которые 100% захотят наш продукт?\n\n'
                                                       'Приведи их к нам и получишь 10% от его заказа! Для этого твой '
                                                       'кореш после оформления просто должен кинуть твой ник '
                                                       'менеджеру, чтобы мы с тобой связались и скинули '
                                                       'вознаграждение.', reply_markup=buttons.backtake_btns())
            elif call.data == 'manager':
                bot.send_message(call.message.chat.id, 'Написать нашему менеджеру - @wakcup', reply_markup=buttons.back_btns())
            elif call.data == 'manager1':
                bot.send_message(user_id, 'Написать нашему менеджеру - @wakcup', reply_markup=buttons.backman_btns())
            elif call.data == 'pizdec':
                with open(image_path1, 'rb') as photo:
                    bot.send_photo(chat_id=user_id, caption='Спасибо за покупку, бро!🫗\n\nЧтобы отслеживать статус посылки, зарегистрируйся в приложении СДЭК с номером телефона, который ты давал ранее.\nЕсли есть вопросы, посмотри в разделе или обратись к менеджеру.\nEnjoy your lean😵‍💫\n', photo=photo, reply_markup=buttons.pay_btns())
            elif call.data[:8] == 'category' and code == 10:
                if call.data[8:] != '<back>':
                    temp_user_data.temp_data(user_id)[user_id][0] = 19
                    temp_user_data.temp_data(user_id)[user_id][5][0] = -1
                    temp_user_data.temp_data(user_id)[user_id][5][1] = call.data[8:]
                    temp_user_data.temp_data(user_id)[user_id][5][2] = db_actions.get_all_product_id()
                    show_product(user_id, '1')
                else:
                    temp_user_data.temp_data(user_id)[user_id][0] = None
                    start_message(user_id)
            elif call.data[:6] == 'switch' and code == 19:
                show_product(user_id, call.data[6:])
            elif call.data[:8] == 'addtobuy':
                temp_user_data.temp_data(user_id)[user_id][4] = call.data[8:]
                if db_actions.check_user_reg(user_id):
                    if db_actions.update_shipping_cart(user_id, call.data[8:]):
                        bot.answer_callback_query(call.id, "Товар добавлен в корзину", show_alert=True)
                    else:
                        bot.answer_callback_query(call.id, "Товар уже в корзине", show_alert=True)
                else:
                    bot.send_message(user_id, 'Для начала нам нужна инфа для доставки, заполни эти данные, потом перейдем к корзине и оплате!\n\nНажми на кнопку "Пройти регистрацию"', reply_markup=buttons.registration_btns())
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
                    db_actions.update_product('categori_id', call.data[8:],
                                              temp_user_data.temp_data(user_id)[user_id][2])
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
                            bot.send_message(user_id, 'Выберите новую категорию',
                                             reply_markup=buttons.categories_btns(categories))
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
                    bot.send_message(user_id, 'Пришлите текст для рассылки!')
                    temp_user_data.temp_data(user_id)[user_id][0] = 18
                elif call.data == 'start':
                    start_message(user_id)

    @bot.message_handler(content_types=['text', 'photo'])
    def text_message(message):
        photo = message.photo
        user_input = message.text
        user_nickname = message.from_user.username
        user_id = message.chat.id
        buttons = Bot_inline_btns()
        code = temp_user_data.temp_data(user_id)[user_id][0]
        if db_actions.user_is_existed(user_id):
            if user_input == 'Начать использование!':
                start_message(user_id)
            elif user_input == 'Ввести данные':
                temp_user_data.temp_data(user_id)[user_id][0] = 12
                bot.send_message(user_id, 'Введите имя', reply_markup=types.ReplyKeyboardRemove())
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
                        bot.send_message(user_id, 'Выберите категорию для товара',
                                         reply_markup=buttons.categories_btns(categories))
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
                        db_actions.update_product('description', user_input,
                                                  temp_user_data.temp_data(user_id)[user_id][2])
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
                case 12:
                    if user_input is not None:
                        try:
                            temp_user_data.temp_data(user_id)[user_id][3].append(user_input)
                            temp_user_data.temp_data(user_id)[user_id][0] = 13
                            bot.send_message(user_id, 'Введите фамилию')
                        except:
                            bot.send_message(user_id, 'Это не номер!')
                case 13:
                    if user_input is not None:
                        try:
                            temp_user_data.temp_data(user_id)[user_id][3].append(user_input)
                            temp_user_data.temp_data(user_id)[user_id][0] = 14
                            bot.send_message(user_id, 'Введите отчество')
                        except:
                            bot.send_message(user_id, 'Это не имя')
                case 14:
                    if user_input is not None:
                        try:
                            temp_user_data.temp_data(user_id)[user_id][3].append(user_input)
                            temp_user_data.temp_data(user_id)[user_id][0] = 15
                            bot.send_message(user_id, 'Введите город')
                        except:
                            bot.send_message(user_id, 'Это не фамилия')
                case 15:
                    if user_input is not None:
                        try:
                            temp_user_data.temp_data(user_id)[user_id][3].append(user_input)
                            temp_user_data.temp_data(user_id)[user_id][0] = 16
                            bot.send_message(user_id, 'Введите адрес сдека')
                        except:
                            bot.send_message(user_id, 'Это не отчество!')
                case 16:
                    if user_input is not None:
                        try:
                            temp_user_data.temp_data(user_id)[user_id][3].append(user_input)
                            temp_user_data.temp_data(user_id)[user_id][0] = 17
                            bot.send_message(user_id, 'Введите номер телефона\n\nВ формате +7')
                        except:
                            bot.send_message(user_id, 'Это не город!')

                case 17:
                    if user_input is not None:
                        temp_user_data.temp_data(user_id)[user_id][3].append(user_input)
                        temp_user_data.temp_data(user_id)[user_id][0] = None
                        db_actions.post_reg_user(user_id, temp_user_data.temp_data(user_id)[user_id][3], f'@{user_nickname}')
                        db_actions.update_shipping_cart(user_id, temp_user_data.temp_data(user_id)[user_id][4])
                        db_actions.update_user_reg(user_id, True)
                        bot.send_message(user_id, 'Вы прошли регистрацию! Товар успешно добавлен в корзину!', reply_markup=buttons.delete_btns())
                case 18:
                    if user_input is not None:
                        userid = db_actions.read_user()
                        for users in userid:
                            try:
                                bot.send_message(users[0], user_input)
                            except:
                                bot.send_message(message.chat.id, 'Ошибка!')
                        bot.send_message(user_id, 'Рассылка успешно отправлена!')
                    else:
                        bot.send_message(message.chat.id, 'Это не текст!')
                case 20:
                    if user_input is not None:
                        try:
                            if db_actions.quanity_shipping_cart(user_id, temp_user_data.temp_data(user_id)[user_id][6], int(user_input)):
                                bot.send_message(user_id, 'Действие успешно завершено', reply_markup=buttons.back_to_cart_btns())
                            else:
                                bot.send_message(user_id, 'Товар отсутствует в вашей корзине!', reply_markup=buttons.back_to_cart_btns())
                        except:
                            bot.send_message(user_id, 'Это не число')

        @bot.shipping_query_handler(func=lambda query: True)
        def shipping(shipping_query):
            bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=[])

        @bot.pre_checkout_query_handler(func=lambda query: True)
        def checkout(pre_checkout_query):
            bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

        @bot.message_handler(content_types=['successful_payment'])
        def got_payment(message):
            image_path = 'thx.png'
            buttons = Bot_inline_btns()
            user_nickname = message.from_user.username
            product = message.successful_payment.invoice_payload
            user_data = db_actions.get_reg_fata(user_id)
            for admin in db_actions.get_all_admins():
                bot.send_message(admin, f'НОВАЯ ПОКУПКА!\n\nПокупатель: @{user_nickname}\n\nКорзина:\n{product}Данные чела:\n\nФамилия: {user_data[1]}\nИмя: {user_data[0]}\nОтчество: {user_data[2]}\nНомер телефона: {user_data[5]}\nГород: {user_data[3]}\nАдрес сдека: {user_data[4]}')
            with open(image_path, 'rb') as photo:
                bot.send_photo(chat_id=message.chat.id, caption="Спасибо за покупку, бро!🫗\n\n"
                                              "Чтобы отслеживать статус посылки, зарегистрируйся в приложении СДЭК с номером телефона, который ты давал ранее.\nЕсли есть вопросы, посмотри в разделе или обратись к менеджеру.\nEnjoy your lean😵‍💫", photo=photo, reply_markup=buttons.pay_btns())
    bot.polling(none_stop=True)


if '__main__' == __name__:
    os_type = platform.system()
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(f'{work_dir}/{config_name}', os_type)
    temp_user_data = TempUserData()
    db = DB(config.get_config()['db_file_name'], Lock())
    db_actions = DbAct(db, config, config.get_config()['xlsx_path'])
    pay = config.get_config()['buy_api']
    bot = telebot.TeleBot(config.get_config()['tg_api'])
    main()
