#!/usr/bin/env python
#-*-coding: utf-8 -*-


if __name__ == '__main__':
	town_list = []
	with open('town_russia.txt', 'r', encoding='utf-8-sig') as f:
		for line in f:
			town_list +=line.splitlines()
	for town in range(len(town_list)):
		town_list[town] = town_list[town].upper()
	letters_unicum = []
	for word in town_list:
		if word[0] not in letters_unicum:
		    letters_unicum.append(word[0])
	
	
	def def_answer(remaining_town, named_town, last_town):
		print(last_town)
		print(last_town[-1])
		print(letters_unicum)
		if last_town[-1] in letters_unicum:
			print(len(remaining_town))
			for towns in remaining_town:
				if towns[0] == last_town[-1]: 
					answer = input('Введите название города: ').upper()
					if answer[0] == last_town[-1]:
						if answer in remaining_town and answer in town_list:
							print(len(remaining_town))
							named_town.append(answer)
							remaining_town.remove(answer)
							print(len(remaining_town))
							if answer[-1] in letters_unicum:
								for towns in remaining_town:
									my_answer = ''
									if towns[0] == answer[-1]:
										my_answer = towns
										named_town.append(my_answer)
										remaining_town.remove(my_answer)
										print(named_town)
										print(len(remaining_town))
										print(my_answer)
										if my_answer[-1] in letters_unicum:
											return def_answer(remaining_town, named_town, my_answer)
										else:
											print(f"Так как города на такую букву {my_answer[-1]} не существует, то я называю город на букву {my_answer[-2]}")
											my_answer = my_answer[:len(my_answer)-1]
											return def_answer(remaining_town, named_town, my_answer)
							else:
								print(f'Город должен быть на букву {last_town[-1]}')
								return def_answer(remaining_town, named_town, my_answer)
						else:
							print(f"Так как города на такую букву {answer[-1]} не существует, то назовиbbb город на букву {answer[-2]}")
							return def_answer(remaining_town, named_town, my_answer)
						return print(named_town)
					elif answer in named_town:
						print(f'Такой город {answer} уже был')
						return def_answer(remaining_town, named_town, last_town)
					else:
						print("Такого города не существует, попробуй ещё раз ввести название города!!!")	
						return def_answer(remaining_town, named_town, last_town)
				
	def game_town(town):
		remaining_town = list(town)
		named_town = []
		while remaining_town:
			answer = input('Введите название города:').upper()
			if answer in remaining_town:
				print(len(remaining_town))
				named_town.append(answer)
				remaining_town.remove(answer)
				print(len(remaining_town))
				if answer[-1] in letters_unicum:
					for towns in remaining_town:
						my_answer = ''
						if towns[0] == answer[-1]:
							my_answer = towns
							named_town.append(my_answer)
							remaining_town.remove(my_answer)
							print(named_town)
							return def_answer(remaining_town, named_town, my_answer)

			else:
				print("Такого города не существует, попробуй ещё раз ввести название города!!!")	
				return game_town(remaining_town)
				
			return print(answer)
	game_town(town_list)