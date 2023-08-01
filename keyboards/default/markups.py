from aiogram.types import ReplyKeyboardMarkup

all_right_message = "Всё верно"
back_message = "Назад"
cancel_message = "Отменить"
comfirm_message = "Подтвердить заказ"


def back_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(back_message)
    return markup


def check_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(back_message, all_right_message)
    return markup


def confirm_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(comfirm_message)
    markup.add(back_message)
    return markup


def submit_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(cancel_message, all_right_message)
    return markup
