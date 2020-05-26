import ephem

from utils import get_keyboard
from handlers import analys_query


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
            'mercury': ephem.constellation(ephem.Mercury(date)),
            'меркурий': ephem.constellation(ephem.Mercury(date)),
            'venus': ephem.constellation(ephem.Venus(date)),
            'венера': ephem.constellation(ephem.Venus(date)),
            'jupiter': ephem.constellation(ephem.Jupiter(date)),
            'юпитер': ephem.constellation(ephem.Jupiter(date)),
            'saturn': ephem.constellation(ephem.Saturn(date)),
            'сатурн': ephem.constellation(ephem.Saturn(date)),
            'uranus': ephem.constellation(ephem.Uranus(date)),
            'уран': ephem.constellation(ephem.Uranus(date)),
            'neptune': ephem.constellation(ephem.Neptune(date)),
            'нептун': ephem.constellation(ephem.Neptune(date))
        }
        """
        if name_planet in planets_solar_system:
            update.message.reply_text(planets_solar_system[name_planet])
        else:
            update.message.reply_text('Такой планеты нет, попробуйте: Mercury, Venus, Mars, Jupiter, Saturn, Uranus, 
            Neptune', reply_markup=get_keyboard())
         """
        if name_planet:
            update.message.reply_text(planets_solar_system[name_planet], reply_markup=get_keyboard())
        else:
            update.message.reply_text(
                'Такой планеты нет, попробуйте: Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune',
                reply_markup=get_keyboard())
