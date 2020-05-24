from glob import glob
import logging
from random import choice
from telegram import KeyboardButton

from utils import get_user_emo, get_keyboard


def change_avatar(bot, update, user_data):
    if 'emo' in user_data:
        del user_data['emo']
    emo = get_user_emo(user_data)
    update.message.reply_text('Готово: {}'.format(user_data['emo']), reply_markup=get_keyboard())


def send_cat_picture(bot, update, user_data):
    cat_list = glob('images/cat*.jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat_id, photo=open(cat_pic, 'rb'))


def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = f"Привет {update.message.chat.first_name} {user_data['emo']}! Ты написал: {update.message.text}"
    logging.info(
        f"User: {update.message.chat.username}, Chat id: {update.message.chat.id}, Message: {update.message.text}")
    # see fields in update message
    # print(update.message)
    update.message.reply_text(user_text, reply_markup=get_keyboard())
    # reply_markup=my_keyboard - вызов клавиатуры


def word_count(bot, update, user_data):
    if analys_query(bot, update):
        update.message.reply_text(f'Количество слов в Вашем запросе: {len(update.message.text.split())-1}')


def analys_query(bot, update):
    if len(update.message.text.split()) == 1 or update.message.text[1] == '':
        update.message.reply_text('Вы ввели пустую строку, попробуйте ещё раз!', reply_markup=get_keyboard())
    else:
        return True


def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text('Готово: {}'.format(get_user_emo(user_data)), reply_markup=get_keyboard())


def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text('Готово: {}'.format(get_user_emo(user_data)), reply_markup=get_keyboard())


def greet_user(bot, update, user_data):
    emo = get_user_emo(user_data)
    text = f'Привет {user_data["emo"]}'
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать координаты', request_location=True)
    user_data['emo'] = emo
    """В настоящее время я могу:
    Обрабатывать команду:
    /planet <имя планеты> - которая запускает функцию constellation_planet и сообщает пользователю в каком созвездии 
    находится запрашиваемя планета на текущую дату. Можно узнать информацию о следующих планетах: Mercury, Venus, Mars, 
    Jupiter, Saturn, Uranus, Neptune.
    Названия планет так же можно вводить на русском языке не зависимо от регистра.

    Или просто получать от Вас любое сообщение, и возвращать Вам его, обращаясь по имени.
    """

    logging.info(text)
    update.message.reply_text(text, reply_markup=get_keyboard())
