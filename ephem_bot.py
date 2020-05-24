from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

from game_town_base_bot import game, clear, calculator, help
from utils import*
from handlers import*
from planet_inform import constellation_planet

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def main():
    """
    Это главная функция бота. Сейчас она умеет обрабатывать команды:
    /start - которая запускает функцию greet_user, выводит сообщение в консоли телеграмма 'Вызван /start' и передаёт в
    log файл информацию
    /planet <имя планеты> - которая запускает функцию constellation_planet и сообщает пользователю в каком созвездии
    находится запрашиваемя планета на текущую дату. Можно узнать информацию о следующих планетах: Mercury, Venus, Earth,
    Mars, Jupiter, Saturn, Uranus, Neptune.
    Так же обрабатывает любой текст от пользователя, сообщая ему по имени, что он записал и отправляет информацию в log
    файл. Это производится при запуске функции talk_to_me.
    Для функционирования бота запускается из модуля telegram.ext функция Updater, которая принимает данные API и
    настройки прокси и запускает два метода:
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
    dp.add_handler(CommandHandler("cities", game, pass_user_data=True))
    dp.add_handler(CommandHandler("clear", clear, pass_user_data=True))
    dp.add_handler(CommandHandler("calc", calculator, pass_user_data=True))
    dp.add_handler(CommandHandler("help", help, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
