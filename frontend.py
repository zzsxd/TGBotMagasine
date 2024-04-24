#####################################
#            Created by             #
#               zzsxd               #
#####################################
import telebot
from telebot import types


#####################################

class Bot_inline_btns:
    def __init__(self):
        super(Bot_inline_btns, self).__init__()
        self.__markup = types.InlineKeyboardMarkup(row_width=1)

    def start_btns(self):
        assortiment = types.InlineKeyboardButton('Ассортимент и цены🛍️', callback_data='assortiment')
        cart = types.InlineKeyboardButton('Корзина🛒', callback_data='cart')
        bonus = types.InlineKeyboardButton('Акции🎁', callback_data='bonus')
        reviews = types.InlineKeyboardButton('Отзывы📝', callback_data='reviews')
        faq = types.InlineKeyboardButton('Ответы на вопросы❓', callback_data='faq')
        self.__markup.add(assortiment, cart, bonus, reviews, faq)
        return self.__markup

    def back_to_cart_btns(self):
        cart = types.InlineKeyboardButton('Корзина🛒', callback_data='cart')
        back = types.InlineKeyboardButton('В главное меню⤵️', callback_data='start')
        self.__markup.add(cart, back)
        return self.__markup
    def pay_btns(self):
        back = types.InlineKeyboardButton('В главное меню⤵️', callback_data='start')
        man = types.InlineKeyboardButton('Написать менеджеру📲', callback_data='manager1')
        self.__markup.add(back, man)
        return self.__markup
    def backman_btns(self):
        back = types.InlineKeyboardButton('Назад⤵️', callback_data='pizdec')
        self.__markup.add(back)
        return self.__markup
    def backdev_btns(self):
        back = types.InlineKeyboardButton('Назад⤵️', callback_data='faq')
        man = types.InlineKeyboardButton('Написать менеджеру📲', callback_data='manager')
        self.__markup.add(back, man)
        return self.__markup

    def startup_btns(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        reg = types.KeyboardButton('Начать использование!')
        keyboard.add(reg)
        return keyboard

    def backkorzina_btns(self):
        cart = types.InlineKeyboardButton('Назад⤵️', callback_data='cart')
        self.__markup.add(cart)
        return self.__markup

    def registration_btns(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        reg = types.KeyboardButton('Ввести данные')
        keyboard.add(reg)
        return keyboard

    def admin_btns(self):
        export = types.InlineKeyboardButton('Экспорт БД', callback_data='export')
        addtovar = types.InlineKeyboardButton('Добавить товар', callback_data='addtovar')
        changetovar = types.InlineKeyboardButton('Изменить товар', callback_data='changetovar')
        newsletter = types.InlineKeyboardButton('Создать рассылку', callback_data='newsletter')
        newsletter1 = types.InlineKeyboardButton('Добавить категорию', callback_data='addcategory')
        del_category = types.InlineKeyboardButton('Удалить категорию', callback_data='delcategory')
        self.__markup.add(export, addtovar, changetovar, newsletter, newsletter1, del_category)
        return self.__markup

    def assortiment_btns(self, categories):
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i in categories:
            btn = types.InlineKeyboardButton(i[1], callback_data=f'category{i[0]}')
            markup.add(btn)
        btn1 = types.InlineKeyboardButton('В главное меню⤵️', callback_data=f'category<back>')
        markup.add(btn1)
        return markup

    def bonus_btns(self):
        take = types.InlineKeyboardButton('Получи 10% от продаж', callback_data='taketenprocents')
        man = types.InlineKeyboardButton('В главное меню⤵️', callback_data='start')
        self.__markup.add(take, man)
        return self.__markup

    def reviews_btns(self):
        link = types.InlineKeyboardButton('Телеграм', url='https://t.me/wakfeedback')
        vk = types.InlineKeyboardButton('ВКонтакте', url='https://vk.com/topic-216187442_50186481')
        avito = types.InlineKeyboardButton('Авито', url='https://www.avito.ru/moskva/posuda_i_tovary_dlya_kuhni/double_cup_bape_3081290746?utm_campaign=native&utm_medium=item_page_ios&utm_source=soc_sharing')
        ozon = types.InlineKeyboardButton('Озон', url='https://www.ozon.ru/seller/wakcup-1529348/products/?miniapp=seller_1529348')
        back = types.InlineKeyboardButton('В главное меню⤵️', callback_data='start')
        self.__markup.add(link, vk, avito, ozon, back)
        return self.__markup

    def add_product_to_shipping_cart(self, product_id):
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('<', callback_data=f'switch2')
        btn2 = types.InlineKeyboardButton('>', callback_data=f'switch1')
        btn3 = types.InlineKeyboardButton('Добавить в корзину🛒', callback_data=f'addtobuy{product_id}')
        btn4 = types.InlineKeyboardButton('Назад⤵️', callback_data='assortiment')
        markup.add(btn1, btn2, btn3, btn4)
        return markup

    def pay_shipping_cart(self):
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('Изменить товар ✏️', callback_data=f'change_shopping_cart')
        btn2 = types.InlineKeyboardButton('Оплатить💳', callback_data=f'pay_shipping_cart')
        btn3 = types.InlineKeyboardButton('Информация о доставке📦', callback_data='delivery1')
        btn4 = types.InlineKeyboardButton('Ассортимент 🛍️', callback_data='assortiment')
        markup.add(btn1, btn2, btn3, btn4)
        return markup

    def shipping_products_change_btns(self, products_names):
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i in products_names:
            btn = types.InlineKeyboardButton(i[0], callback_data=f'changeproduct_cart{i[1]}')
            markup.add(btn)
        return markup

    def shipping_products_delete_btns(self):
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('Изменить количество✏️', callback_data=f'quanity_shopping_cart')
        btn2 = types.InlineKeyboardButton('Удалить❌', callback_data=f'delete_shopping_cart')
        markup.add(btn1, btn2)
        return markup

    def categories_btns(self, categories):
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i in categories:
            btn = types.InlineKeyboardButton(i[1], callback_data=f'category{i[0]}')
            markup.add(btn)
        return markup

    def product_btns(self, categories):
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i in categories:
            btn = types.InlineKeyboardButton(i[1], callback_data=f'change_product{i[0]}')
            markup.add(btn)
        return markup

    def change_peoduct_btns(self):
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn = types.InlineKeyboardButton('Название', callback_data=f'finally_change_product1')
        btn1 = types.InlineKeyboardButton("Описание", callback_data=f'finally_change_product2')
        btn2 = types.InlineKeyboardButton("Фото", callback_data=f'finally_change_product3')
        btn3 = types.InlineKeyboardButton("Категорию", callback_data=f'finally_change_product4')
        btn4 = types.InlineKeyboardButton("Цену", callback_data=f'finally_change_product5')
        markup.add(btn, btn1, btn2, btn3, btn4)
        return markup

    def faq_btns(self):
        one = types.InlineKeyboardButton('Заказ и оплата💳', callback_data='order')
        two = types.InlineKeyboardButton('Доставка 📦', callback_data='delivery')
        three = types.InlineKeyboardButton('Легально?💊', callback_data='legal')
        four = types.InlineKeyboardButton('Все про сиропы🫗', callback_data='sirop')
        five = types.InlineKeyboardButton('Гарантии✅', callback_data='guarantees')
        six = types.InlineKeyboardButton('Написать менеджеру 📲', callback_data='manager')
        seven = types.InlineKeyboardButton('Заказ не отправлен больше недели ⏳', callback_data='notdelivery')
        back = types.InlineKeyboardButton('В главное меню⤵️', callback_data='start')
        self.__markup.add(one, two, three, seven, four, five, six, back)
        return self.__markup
    def guarantees_btns(self):
        one = types.InlineKeyboardButton('Посмотреть отзывы👀', callback_data='reviews')
        two = types.InlineKeyboardButton('Назад⤵️', callback_data='faq')
        self.__markup.add(one, two)
        return self.__markup

    def back_btns(self):
        back = types.InlineKeyboardButton('Назад⤵️', callback_data='faq')
        self.__markup.add(back)
        return self.__markup
    def backorder_btns(self):
        back = types.InlineKeyboardButton('Доставка📦', callback_data='delivery')
        buton = types.InlineKeyboardButton('Назад⤵️', callback_data='faq')
        self.__markup.add(back, buton)
        return self.__markup
    def backtake_btns(self):
        back = types.InlineKeyboardButton('Назад⤵️', callback_data='bonus')
        man = types.InlineKeyboardButton('Написать менеджеру📲', callback_data='manager')
        self.__markup.add(back, man)
        return self.__markup
    def delete_btns(self):
        a = telebot.types.InlineKeyboardButton('В корзину🛒', callback_data='cart')
        self.__markup.add(a)
        return self.__markup
