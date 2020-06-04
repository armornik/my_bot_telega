from emoji import emojize
from clarifai.rest import ClarifaiApp
from random import choice
from telegram import ReplyKeyboardMarkup, KeyboardButton

import settings_bot


def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать координаты', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
        ['Прислать котика', 'Сменить аватарку'],
        [contact_button, location_button],
        ['Заполнить анкету', ]
                                       ], resize_keyboard=True)
    return my_keyboard


def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings_bot.USER_EMOJI), use_aliases=True)


def is_cat(file_name):
    image_has_cat = False
    app = ClarifaiApp(api_key=settings_bot.CLARIFAI_API_KEY)
    model = app.public_models.general_model
    response = model.predict_by_filename(file_name, max_concepts=5)
    # import pprint
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(response)
    if response['status']['code'] == 10000:
        for concept in response['outputs'][0]['data']['concepts']:
            if concept['name'] == 'cat':
                print('Cat is here!')
                image_has_cat = True
    return image_has_cat


if __name__ == '__main__':
    print(is_cat('images/cat3.jpeg'))
    print(is_cat('images/cat4.jpeg'))
