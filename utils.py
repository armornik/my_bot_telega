from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from random import choice

import settings_bot


def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать координаты', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
        ['Прислать котика', 'Сменить аватарку'],
        [contact_button, location_button]
                                       ], resize_keyboard=True)
    return my_keyboard


def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings_bot.USER_EMOJI), use_aliases=True)