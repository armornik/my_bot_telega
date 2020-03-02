from glob import glob
import logging
from random import choice

import ephem
from telegram import update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings_bot



town_list = []
with open('town_russia.txt', 'r', encoding='utf-8') as f:
	for line in f:
		town_list +=line.splitlines()
CITIES = list(map(lambda x:x.upper(), town_list))
letters_unikum = []
for word in CITIES:
	if word[0] not in letters_unikum:
		letters_unikum.append(word[0])


def availability_town(town, index, winner, remaining_cities, update):
	remaining_cities.remove(town)
	for i in remaining_cities:
		#found = ''
		if i[0] == town[index]:
			update.message.reply_text(f'Мой ход: {i}')
			remaining_cities.remove(i)
			town = i
			break
	if town:
		if town[-1] in letters_unikum:
			update.message.reply_text(f'Ваш ход на букву {town[-1]}')
			game(town[-1], town, update) #этот вызов обнуляет список городов remaining_cities
		else:
			print(f'Так как города на букву {town[-1]} нет, то вы называете город на букву {town[-2]}')
			game(town[-2], town) #этот вызов обнуляет список городов remaining_cities
	else:
		update.message.reply_text(town)
		update.message.reply_text(f'Города на {town[0]} закончились')
		update.message.reply_text(winner)


def game(letter, first_cities, update):
	remaining_cities = list(CITIES)
	if letter:
		while True:
			town = input(update.message.reply_text(f'Введите город: на букву {letter}\n')).upper()
			if town[0] != letter:
				print('Неверный ввод, не та буква в начале')
				continue
			else:
				break
	else:
		if first_cities:
			town = first_cities
		else:
			town = update.message.reply_text(input('Введите город: ')).upper()
	if town in remaining_cities:
		if town[-1] in letters_unikum:
			availability_town(town, -1, 'Я победил', remaining_cities, update)
		else:
			update.message.reply_text(print(f'Так как города на букву {town[-1]} нет, то я называю город на букву {town[-2]}'))
			availability_town(town, -2, 'Вы победили', remaining_cities, update)
	else:
		update.message.reply_text(f'Нет такого города\n')
		game('', '')


if __name__ == '__main__':
	game('','', update)
