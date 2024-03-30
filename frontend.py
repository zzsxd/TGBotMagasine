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
        assortiment = types.InlineKeyboardButton('Ассортимент и цены', callback_data='assortiment')
        cart = types.InlineKeyboardButton('Корзина', callback_data='cart')
        bonus = types.InlineKeyboardButton('Акции', callback_data='bonus')
        reviews = types.InlineKeyboardButton('Отзывы', callback_data='reviews')
        faq = types.InlineKeyboardButton('Ответы на вопросы', callback_data='faq')
        self.__markup.add(assortiment, cart, bonus, reviews, faq)
        return self.__markup

    def admin_btns(self):
        export = types.InlineKeyboardButton('Экспорт БД', callback_data='export')
        addtovar = types.InlineKeyboardButton('Добавить товар', callback_data='addtovar')
        changetovar = types.InlineKeyboardButton('Изменить товар', callback_data='changetovar')
        newsletter = types.InlineKeyboardButton('Создать рассылку', callback_data='newsletter')
        self.__markup.add(export, addtovar, changetovar, newsletter)
        return self.__markup

    def assortiment_btns(self):
        doublecups = types.InlineKeyboardButton('Double Cups', callback_data='doublecups')
        sizzurps = types.InlineKeyboardButton('Sizzurps', callback_data='sizzurps')
        sets = types.InlineKeyboardButton('Sets', callback_data='sets')
        other = types.InlineKeyboardButton('Other', callback_data='other')
        self.__markup.add(doublecups, sizzurps, sets, other)
        return self.__markup

    def bonus_btns(self):
        take = types.InlineKeyboardButton('Получи 10% от продаж', callback_data='taketenprocents')
        self.__markup.add(take)
        return self.__markup

    def reviews_btns(self):
        link = types.InlineKeyboardButton('Отзывы', url='vk.com')
        vk = types.InlineKeyboardButton('Отзывы ВК', url='vk.com')
        avito = types.InlineKeyboardButton('Отзывы Авито', url='vk.com')
        ozon = types.InlineKeyboardButton('Озон', url='vk.com')
        self.__markup.add(link, vk, avito, ozon)
        return self.__markup

    def faq_btns(self):
        one = types.InlineKeyboardButton('Заказ и оплата', callback_data='order')
        two = types.InlineKeyboardButton('Доставка', callback_data='delivery')
        three = types.InlineKeyboardButton('Легально?', callback_data='legal')
        four = types.InlineKeyboardButton('Все про сиропы', callback_data='sirop')
        five = types.InlineKeyboardButton('Гарантии', callback_data='guarantees')
        six = types.InlineKeyboardButton('Написать менеджеру', callback_data='manager')
        seven = types.InlineKeyboardButton('Заказ не отправлен больше недели', callback_data='notdelivery')
        self.__markup.add(one, two, three, seven, four, five, six)
        return self.__markup

