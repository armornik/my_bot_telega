import sqlite3

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()
# delete old table and create new with two column
# cursor.execute("DROP TABLE IF EXISTS towns")
# cursor.execute("CREATE TABLE IF NOT EXISTS towns (town varchar(255), is_used int) ")
cursor.execute("CREATE TABLE IF NOT EXISTS game_data (id_user varchar(255), last_word varchar(255)) ")

if __name__ == '__main__':
    town_list = []
    # Null column is_used
    cursor.execute('UPDATE towns SET is_used = 0')
    # filling table when new
    # with open('town_russia.txt', 'r', encoding='utf-8') as f:
    #     for line in f:
    #         cursor.execute("INSERT INTO towns VALUES ('{t}',{u})".format(t=line.upper().rstrip("\n"), u=0))
    #         conn.commit()
    #         pass


def game(ide, town, update):
    town = town.upper()
    # check id it table
    print(ide)
    print(town)
    print(update)
    cursor.execute("SELECT * FROM game_data WHERE id_user = '{i}'".format(i=ide))
    check_id = cursor.fetchone()
    print(3)
    if check_id:
        cursor.execute("SELECT last_word FROM game_data WHERE id = '{i}'".format(i=ide))
        last_word = cursor.fetchone()
        for i in last_word[::-1]:
            cursor.execute("SELECT * FROM towns WHERE substr(town,1,1) = '{let}' AND is_used = 0 LIMIT 1".format(let=i))
            res = cursor.fetchone()
            if res:
                if res[0][-1] in ('Ь', ' ', 'Ы', 'Ъ'):
                    check_letter = res[0][-2]
                    letter = town[0]
                    if check_letter != letter:
                        update.message.reply_text(
                            f'Неверный ввод, не та буква в начале, Вам необходимо ввести город на букву {check_letter}')
                    else:
                        # check town it table
                        cursor.execute("SELECT * FROM towns WHERE town = '{t}'".format(t=town))
                        # get first result
                        res = cursor.fetchone()
                        if res:
                            if res[1] == 1:
                                update.message.reply_text("Такой город уже называли")
                            else:
                                cursor.execute("UPDATE towns SET is_used = 1 WHERE town = '{t}'".format(t=town))
                                conn.commit()
                                for i in town[::-1]:
                                    cursor.execute(
                                        "SELECT * FROM towns WHERE substr(town,1,1) = '{let}' AND is_used = 0 LIMIT 1".format(
                                            let=i))
                                    res = cursor.fetchone()
                                    if res:
                                        if res[0][-1] in ('Ь', ' ', 'Ы', 'Ъ'):
                                            game(res[0][-2])
                                        else:
                                            game(res[0][-1])
                                    print(f'Городов на {i} нет, смотрю дальше')
                                print('Ты выиграл, городов больше нет')
                                exit(0)
    # check town it table
    cursor.execute("SELECT * FROM towns WHERE town = '{t}'".format(t=town))
    res = cursor.fetchone()
    print(1)
    if res:
        if res[1] == 1:
            update.message.reply_text("Такой город уже называли")
        else:
            cursor.execute("UPDATE towns SET is_used = 1 WHERE town = '{t}'".format(t=town))
            cursor.execute("UPDATE game_data SET id_used = '{i} WHERE id_used = '{i}'".format(i=ide))
            conn.commit()
            for i in town[::-1]:
                cursor.execute("SELECT * FROM towns WHERE substr(town,1,1) = '{let}' AND is_used = 0 LIMIT 1".format(let=i))
                res = cursor.fetchone()
                if res:
                    print("Мой ход: " + res[0])
                    cursor.execute("UPDATE towns SET is_used = 1 WHERE town = '{t}'".format(t=res[0]))
                    cursor.execute(
                        "UPDATE game_data SET id_used = '{i}', last_word = {t}  WHERE id_used = '{i}'".format(i=id, t=res[0]))
                    conn.commit()
                    if res[0][-1] in ('Ь', ' ', 'Ы', 'Ъ'):
                        update.message.reply_text(f'Мой ход: {res[0]}\n Назови город на букву {res[0][-2]}')
                    else:
                        update.message.reply_text(f'Мой ход: {res[0]}\n Назови город на букву {res[0][-1]}')
                update.message.reply_text(f'Городов на {i} нет, смотрю дальше')
            update.message.reply_text('Ты выиграл, городов больше нет')
    else:
        print(2)
        update.message.reply_text('Нет такого города')