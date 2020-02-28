import logging
import ephem
import settings_bot

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def constellation_planet(bot, update):
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


def greet_user(bot, update):
    text = """В настоящее время я могу:
	Обрабатывать команду:
	/planet <имя планеты> - которая запускает функцию constellation_planet и сообщает пользователю в каком созвездии находится запрашиваемя
		планета на текущую дату. Можно узнать информацию о следующих планетах: Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune.
		Названия планет так же можно вводить на русском языке не зависимо от регистра.
	
	Или просто получать от Вас любое сообщение, и возвращать Вам его, обращаясь по имени.
	"""
    logging.info(text)
    update.message.reply_text(text)


def talk_to_me(bot, update):
    user_text = f"Привет {update.message.chat.first_name}! Ты написал: {update.message.text}"
    logging.info(
        f"User: {update.message.chat.username}, Chat id: {update.message.chat.id}, Message: {update.message.text}")
    print(update.message)
    update.message.reply_text(user_text)


def word_count(bot, update):
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
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", constellation_planet))
    dp.add_handler(CommandHandler("wordcount", word_count))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
