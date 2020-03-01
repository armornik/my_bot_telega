from glob import glob
import logging
from random import choice

from emoji import emojize
import ephem
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

import settings_bot

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


# def game_town_user(bot, update, user_data):
#     if analys_query(bot, update):
#         cities1 = update.message.text.split(' ')[1].strip().upper()
#         update.message.reply_text(f'{game("", cities1)}!\n')


def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings_bot.USER_EMOJI), use_aliases=True)


def change_avatar(bot, update, user_data):
    if 'emo' in user_data:
        del user_data['emo']
    emo = get_user_emo(user_data)
    update.message.reply_text('Готово: {}'.format(user_data['emo']))


def send_cat_picture(bot, update, user_data):
    cat_list = glob('images/cat*.jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat_id, photo=open(cat_pic, 'rb'))


def constellation_planet(bot, update, user_data):
    if analys_query(bot, update):
    # name_planet = update.message.text.split(' ')[1].strip().lower()

        name_planet: str = update.message.text.split(' ')[1].strip().lower()
        # date = str(update.message.date).split(' ')[0].replace('-', '/')
        date = update.message.date.strftime('%d/%m/%Y')


        # planets_solar_system = {
        #     ephem.constellation(ephem.Mars(date)): ('mars', 'марс'),
        #     ephem.constellation(ephem.Mercury(date)): ('mercury', 'меркурий'),
        # }

        planets_solar_system = {
        'mars': ephem.constellation(ephem.Mars(date)),
        'марс': ephem.constellation(ephem.Mars(date)),
        'mercury' : ephem.constellation(ephem.Mercury(date)),
        'меркурий' : ephem.constellation(ephem.Mercury(date)),
        'venus' : ephem.constellation(ephem.Venus(date)),
        'венера' : ephem.constellation(ephem.Venus(date)),
        'jupiter' : ephem.constellation(ephem.Jupiter(date)),
        'юпитер' : ephem.constellation(ephem.Jupiter(date)),
        'saturn' : ephem.constellation(ephem.Saturn(date)),
        'сатурн' : ephem.constellation(ephem.Saturn(date)),
        'uranus' : ephem.constellation(ephem.Uranus(date)),
        'уран' : ephem.constellation(ephem.Uranus(date)),
        'neptune' : ephem.constellation(ephem.Neptune(date)),
        'нептун' : ephem.constellation(ephem.Neptune(date))
        }
        """
        if name_planet in planets_solar_system:
            update.message.reply_text(planets_solar_system[name_planet])
        else:
            update.message.reply_text('Такой планеты нет, попробуйте: Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune')
         """
        if name_planet:
            update.message.reply_text(planets_solar_system[name_planet])
        else:
            update.message.reply_text(
                'Такой планеты нет, попробуйте: Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune')


def greet_user(bot, update, user_data):
    emo = get_user_emo(user_data)
    text = f'Привет {user_data["emo"]}'
    user_data['emo'] = emo
    my_keyboard = ReplyKeyboardMarkup([['Прислать котика', 'Сменить аватарку']])
    """В настоящее время я могу:
	Обрабатывать команду:
	/planet <имя планеты> - которая запускает функцию constellation_planet и сообщает пользователю в каком созвездии находится запрашиваемя
		планета на текущую дату. Можно узнать информацию о следующих планетах: Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune.
		Названия планет так же можно вводить на русском языке не зависимо от регистра.
	
	Или просто получать от Вас любое сообщение, и возвращать Вам его, обращаясь по имени.
	"""
    logging.info(text)
    update.message.reply_text(text, reply_markup=my_keyboard)


def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = f"Привет {update.message.chat.first_name} {user_data['emo']}! Ты написал: {update.message.text}"
    logging.info(
        f"User: {update.message.chat.username}, Chat id: {update.message.chat.id}, Message: {update.message.text}")
    # see fields in update message
    #print(update.message)
    update.message.reply_text(user_text)


def word_count(bot, update, user_data):
    if analys_query(bot, update):
        update.message.reply_text(f'Количество слов в Вашем запросе: {len(update.message.text.split())-1}')


def analys_query(bot, update):
    if len(update.message.text.split()) == 1 or update.message.text[1] == '':
        update.message.reply_text("Вы ввели пустую строку, попробуйте ещё раз!")
    else:
        return True




def main():
    """
	Это главная функция бота. Сейчас она умеет обрабатывать команды:

	/start - которая запускает функцию greet_user, выводит сообщение в консоли телеграмма 'Вызван /start' и передаёт в log файл информацию

	/planet <имя планеты> - которая запускает функцию constellation_planet и сообщает пользователю в каком созвездии находится запрашиваемя
		планета на текущую дату. Можно узнать информацию о следующих планетах: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune.

	Так же обрабатывает любой текст от пользователя, сообщая ему по имени, что он записал и отправляет информацию в log файл. Это производится
		при запуске функции talk_to_me.

	Для функционирования бота запускается из модуля telegram.ext функция Updater, которая принимает данные API и настройки прокси и запускает два метода:
	start_polling() - непосредственно запуск работы бота
	idle() - поддержка работоспособности бота пока не прервать, или произойдёт критическая ошибка в работе.
	"""

    mybot = Updater(settings_bot.API, request_kwargs=settings_bot.PROXY)

    logging.info("Бот запускается")

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler("planet", constellation_planet, pass_user_data=True))
    dp.add_handler(CommandHandler("wordcount", word_count, pass_user_data=True))
    dp.add_handler(CommandHandler("cat", send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать котика)$', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить аватарку)$', change_avatar, pass_user_data=True))
    # dp.add_handler(CommandHandler("cities", game_town_user, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
