from glob import glob
import logging
import os
from random import choice
from telegram import KeyboardButton, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from utils import get_user_emo, get_keyboard, is_cat


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


def check_user_photo(bot, update, user_data):
    update.message.reply_text('Обрабатываю фото')
    os.makedirs('downloads', exist_ok=True)
    # photo_file - взять оригинальный файл, а не превью, которые создаёт телеграмм
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('downloads', '{}.jpg'.format(photo_file.file_id))
    photo_file.download(filename)
    update.message.reply_text('Файл сохранён')
    if is_cat(filename):
        update.message.reply_text('Обнаружен котик, добавляю в библиотеку.')
        new_filename = os.path.join('images', 'cat_{}.jpg'.format(photo_file.file_id))
        os.rename(filename, new_filename)
    else:
        # os.remove(filename)
        update.message.reply_text('Котика нет на фото')


def anketa_start(bot, update, user_data):
    # reply_markup = ReplyKeyboardRemove() - скрывает клавиатуру
    update.message.reply_text('Как Вас зовут? Напишите имя и фамилию', reply_markup=ReplyKeyboardRemove())
    return 'name'


def anketa_get_name(bot, update, user_data):
    user_name = update.message.text
    if len(user_name.split(' ')) != 2:
        update.message.reply_text('Пожалуйста введите имя и фамилию')
        return 'name'
    else:
        user_data['anketa_name'] = user_name
        reply_keyboard = [['1', '2', '3', '4', '5']]
        # one_time_keyboard = True - скрыть клавиатуру после оценки работы бота
        update.message.reply_text('Оцените качество бота от 1 до 5',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard), one_time_keyboard=True)
        return 'rating'


def anketa_rating(bot, update, user_data):
    user_data['anketa_rating'] = update.message.text
    update.message.reply_text('''Пожалуйста напишите отзыв в свободной форме 
или введите /skip чтобы пропустить''')
    return 'comment'


def anketa_comment(bot, update, user_data):
    user_data['anketa_comment'] = update.message.text
    user_text = '''
<b>Имя Фамилия: </b> {anketa_name}
<b>Оценка: </b> {anketa_rating}
<b>Комментарий: </b> {anketa_comment}'''.format(**user_data)
    update.message.reply_text(user_text, reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def anketa_skip_comment(bot, update, user_data):
    user_data['anketa_comment'] = update.message.text
    user_text = '''
<b>Имя Фамилия: </b> {anketa_name}
<b>Оценка: </b> {anketa_rating}'''.format(**user_data)
    update.message.reply_text(user_text, reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def dont_know(bot, update, user_data):
    update.message.reply_text('Я не понимаю')
