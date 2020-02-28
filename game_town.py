#!/usr/bin/env python

if __name__ == '__main__':
	town_list = []
	with open('town_russia.txt', 'r', encoding='utf-8-sig') as f:
		for line in f:
			town_list +=line.splitlines()
	d = list(map(lambda x:x.upper(), town_list))
	letters_unikum = []
	for word in d:
		if word[0] not in letters_unikum:
			letters_unikum.append(word[0])


def game(letter):
	if letter:
		while True:
			town = input(f'Введите город: на букву {letter}\n').upper()
			if town[0] != letter:
				print('Неверный ввод, не та буква в начале')
				continue
			else:
				break
	else:
		town = input('Введите город: ').upper()
	if town in d:
		if town[-1] in letters_unikum:

			d.remove(town)
			for i in d:
				found=''
				if i[0] == town[-1]:
					print(f'Мой ход: {i}')
					d.remove(i)
					found=i
					break
			if found:
				if i[-1] in letters_unikum:
					print(f'Ваш ход на букву {i[-1]}')
					game(i[-1])
				else:
					print(f'Так как города на букву {i[-1]} нет, то вы называете город на букву {i[-2]}')
					game(i[-2])
			else:
				print(i)
				print(f'Города на {i[0]} закончились')
				return 'Я победил'
		else:
			print(f'Так как города на букву {town[-1]} нет, то я называю город на букву {town[-2]}')
			d.remove(town)
			for i in d:
				found=''
				if i[0] == town[-2]:
					print(f'Мой ход: {i}')
					d.remove(i)
					found = i
					break
			if found:
				if i[-1] in letters_unikum:
					print(f'Ваш ход на букву {i[-1]}')
					game(i[-1])
				else:
					print(f'Так как города на букву {i[-1]} нет, то вы называете город на букву {i[-2]}')
					game(i[-2])
			else:
				print(i)
				print(f'Города на {+i[0]} закончились')
				return 'Вы победили'
	else:
		print('Нет такого города в списке')
		return game('')


game('')
