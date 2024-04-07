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
from threading import Lock
import time
from config_parser import ConfigParser
from frontend import Bot_inline_btns
from backend import TempUserData, DbAct
from db import DB


def start_message(user_id):
    buttons = Bot_inline_btns()
    bot.send_message(user_id, 'hui',
                     reply_markup=buttons.start_btns())


def main():
    @bot.message_handler(commands=['start', 'admin'])
    def start_msg(message):
        name_user = message.from_user.first_name
        user_id = message.from_user.id
        buttons = Bot_inline_btns()
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
            bot.send_message(user_id, 'Wassup и добро пожаловать в Wakcup Shop!\n'
                                      'Я помогу тебе оформить заказ и ответить на вопросы.\n\n'
                                      'Но для начала, тебе необходимо пройти регистрацию!\n\n'
                                      'Потом по данным которые ты введешь, мы отправим тебе посылку!',
                             reply_markup=buttons.registration_btns())

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
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
                shipping_cart = db_actions.get_shipping_cart_by_user_id(user_id)
                for i in range(len(shipping_cart)):
                    product = db_actions.get_product_by_id(shipping_cart[i])
                    all_cost += int(product[1])
                    s += f'{i + 1}. {product[0]} - {product[1]}\n'
                bot.send_message(user_id, f'Ваша корзина:\n{s}\n\nобщая цена товаров: {all_cost}',
                                 reply_markup=buttons.pay_shipping_cart())
            elif call.data == 'bonus':
                bot.send_message(call.message.chat.id, 'Наши скидки и акции', reply_markup=buttons.bonus_btns())
            elif call.data == 'pay_shipping_cart':
                bot.send_message(call.message.chat.id, 'Кода нет - тимлид уснул')
            elif call.data == 'reviews':
                bot.send_message(call.message.chat.id,
                                 'Мы работаем уже год, и за это время отправили тысячи посылок и собрали сотни отзывов, можешь их чекнуть!\n'
                                 'Так же, у нас работает правило: если мы не отправляем заказ в течение недели, мы дарим тебе сироп, кидаем его в посылку без доплат.',
                                 reply_markup=buttons.reviews_btns())
            elif call.data == 'faq':
                bot.send_message(call.message.chat.id, 'Ответы на все вопросы', reply_markup=buttons.faq_btns())
            elif call.data == 'order':
                bot.send_message(call.message.chat.id, 'Оформление осуществляется через этот бот, для этого зайди в '
                                                       '"Ассортимент и цены" -> выбери товары и добавь их в корзину '
                                                       '-> перейди в корзину, и нажми "Купить", далее нужно указать '
                                                       'свои данные для получения и провести оплату.\n'
                                                       'Оплата осуществляется за товар во время оформления, '
                                                       'а за доставку при получении, примерную стоимость можете '
                                                       'посмотреть тут ( ссылка )')
            elif call.data == 'delivery':
                bot.send_message(call.message.chat.id, 'Доставка осуществляется транспортной компанией СДЭК почти по '
                                                       'всему миру до пункта выдачи ( выбираете сами, там же ее и '
                                                       'оплачиваете при получении), получение по паспорту или СДЭК '
                                                       'id. Есть возможность отправки почтой РФ, если так будет '
                                                       'выгоднее для покупателя.\n'
                                                       'Вот примерная стоимость доставки ( все зависит от заказа ) по '
                                                       'городам:\n'
                                                       'Москва и МО - 370р. / 1-2 раб. дня\n'
                                                       'СПБ - 398р. / 2-3 раб. дня\n'
                                                       'Минск - 485р. / 4-5 раб. дней\n'
                                                       'Новосибирск - 543р. / 3-5 раб. дней\n'
                                                       'Екатеринбург - 415р. / 3-4 раб. дня\n'
                                                       'Астрахань - 429р. / 3-5 раб. дней\n'
                                                       'Ростов-на-Дону - 389р. / 3-4 раб. дня\n'
                                                       'Красноярск - 575р. / 5-7раб. дней\n'
                                                       'Казань - 389р. / 2-3 раб. дня\n'
                                                       'Нижний Новгород - 389р. / 2-3 раб. дня\n'
                                                       'Самара - 398р. / 3-4 раб. дня\n'
                                                       'Краснодар -398р. / 3-4 раб. дня\n'
                                                       'Пенза - 416р. / 2-3 раб. дня\n'
                                                       'Иркутск - 655р. / 9-11 раб. дней\n'
                                                       'Южно-Сахалинск - 719р. / 23-25 раб. дней\n'
                                                       'Омск - 560р. / 4-6 раб. дней\n'
                                                       'Ярославль - 389р. / 2-3 раб. дня\n'
                                                       'Челябинск - 380р. / 3-4 раб. дня\n'
                                                       'Сыктывкар - 414р. / 3-4 раб. дня\n'
                                                       'Если вашего города тут нет, но он находится рядом с одним из '
                                                       'вышеперечисленных, то цена и сроки доставки сильно не '
                                                       'изменятся, не надо писать по такому поводу менеджеру, '
                                                       'если только вам совсем принципиально.')
            elif call.data == 'legal':
                bot.send_message(call.message.chat.id, 'Да, это абсолютно легально и безопасно, вас никто не примет '
                                                       'на пункте выдачи. В составе сиропа нет кодеина, прометазина и '
                                                       'других запрещенных веществ, так что он абсолютно легален, '
                                                       'эффект создает мелатонин, который успокаивает, '
                                                       'вызывает сонливость, расслабляет и клонит в сон.\n'
                                                       'Есть еще элементы, которые придают вкус и запах похожий на '
                                                       'оригинальный американский сироп, но эффект не будет сильным, '
                                                       'т.к. мы не можем сделать легально сильный эффект.')
            elif call.data == 'sirop':
                bot.send_message(call.message.chat.id, 'Мы производим сироп для разбавления со спрайтом, чтобы '
                                                       'получился напиток, похожий на лин, но абсолютно легально. '
                                                       'Чтобы получился готовый напиток, необходимо залить 1/3 или '
                                                       '1/2 в спрайт 0,5, взболтать, перелить все в дабл кап, '
                                                       'добавить джолли ранчерс (на свое усмотрение), добавить лед. '
                                                       'Все, "линчик" готов. В составе сиропа нет кодеина, '
                                                       'прометазина и других запрещенных веществ, так что он '
                                                       'абсолютно легален, эффект создает мелатонин, '
                                                       'который успокаивает, вызывает сонливость, расслабляет и '
                                                       'клонит в сон.\n'
                                                       'Есть еще элементы, которые придают вкус и запах похожий на '
                                                       'оригинальный американский сироп, но эффект не будет сильным, '
                                                       'тк мы не можем сделать легально сильный эффект.')
            elif call.data == 'notdelivery':
                bot.send_message(call.message.chat.id, 'У нас работает правило: если мы не отправляем заказ в течение '
                                                       'недели, мы дарим тебе сироп, кидаем его в посылку без доплат.\n'
                                                       'Если ты ждешь больше недели, то обратись к нашему менеджеру '
                                                       'по кнопке ниже, и мы закинем тебе доп сироп')
            elif call.data == 'guarantees':
                bot.send_message(call.message.chat.id, 'Мы работаем уже год, и за это время отправили тысячи посылок'
                                                       ' и собрали сотни отзывов, можешь их чекнуть!',
                                 reply_markup=buttons.guarantees_btns())
            elif call.data == 'taketenprocents':
                bot.send_message(call.message.chat.id, 'Ты знаешь кентов, которые 100% захотят наш продукт?\n\n'
                                                       'Приведи их к нам и получишь 10% от его заказа! Для этого твой '
                                                       'кореш после оформления просто должен кинуть твой ник '
                                                       'менеджеру, чтобы мы с тобой связались и скинули '
                                                       'вознаграждение.')
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

    @bot.message_handler(content_types=['text', 'photo'])
    def text_message(message):
        photo = message.photo
        user_input = message.text
        user_id = message.chat.id
        buttons = Bot_inline_btns()
        code = temp_user_data.temp_data(user_id)[user_id][0]
        if db_actions.user_is_existed(user_id):
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
        else:
            if user_input == 'Пройти регистрацию!':
                temp_user_data.temp_data(user_id)[user_id][0] = 12
                bot.send_message(user_id, 'Введите имя')
            match code:
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
                            bot.send_message(user_id, "Нажмите на кнопку, чтобы отправить свой номер телефона.",
                                             reply_markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                            one_time_keyboard=True).add(
                                                 telebot.types.KeyboardButton('Отправить номер телефона',
                                                                              request_contact=True)))
                        except:
                            bot.send_message(user_id, 'Это не город!')

    @bot.message_handler(content_types=['contact'])
    def handle_contact(message):
        user_id = message.chat.id
        user_nickname = message.from_user.username
        phone_number = message.contact.phone_number
        if temp_user_data.temp_data(user_id)[user_id][0] == 17:
            temp_user_data.temp_data(user_id)[user_id][3].append(phone_number)
            db_actions.add_user(user_id, temp_user_data.temp_data(user_id)[user_id][3], f'@{user_nickname}')
            bot.send_message(user_id, 'Вы прошли регистрацию!')
            time.sleep(1)
            start_message(user_id)

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
