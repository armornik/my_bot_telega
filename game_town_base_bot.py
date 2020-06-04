import sqlite3

# # delete old table and create new with two column
# conn = sqlite3.connect("mydatabase.db")
# cursor = conn.cursor()
# cursor.execute("DROP TABLE IF EXISTS towns")
# cursor.execute("CREATE TABLE IF NOT EXISTS towns (town varchar(255), is_used int) ")
# cursor.execute("CREATE TABLE IF NOT EXISTS users (username varchar(255), last_town varchar(255), lastletter varchar(255)) ")
#
# if __name__ == '__main__':
#     # Null column is_used
#     cursor.execute('UPDATE towns SET is_used = 0')
#     # filling table when new
#     with open('town_russia.txt', 'r', encoding='utf-8') as f:
#         for line in f:
#             cursor.execute("INSERT INTO towns VALUES ('{t}',{u})".format(t=line.upper().rstrip("\n"), u=0))
#             conn.commit()
#             pass


def game(bot, update, user_data):
    def my_move(town, username):
        for i in town[::-1]:
            res3 = cursor.execute(
                "SELECT * FROM towns WHERE substr(town,1,1) = '{let}' AND is_used = 0 LIMIT 1".format(
                    let=i)).fetchone()
            if res3:
                update.message.reply_text('My answer: ' + res3[0])
                last_letter = res3[0][-1] if res3[0][-1] not in ['Ь', 'Ъ', 'Ы', ' '] else res3[0][-2]
                res4 = cursor.execute(
                    "UPDATE users SET last_town = '{t}', lastletter = '{ll}' WHERE username = '{u}'".format(
                        u=username, t=res3[0], ll=last_letter))
                conn.commit()
                res55 = cursor.execute("UPDATE towns SET is_used = 1 WHERE town = '{t}'".format(t=res3[0]))
                conn.commit()
                return
            update.message.reply_text('No cities on ' + i + ', searching next...')
        update.message.reply_text('No cities on ' + i + ', you win')

    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    try:  # Is input not blank?
        town = update['message']['text'].split()[1].upper()
    except:
        update.message.reply_text('A Town Game. Input town. If u want to reset towns, give command /clear. See /help')
        return

    username = update['message']['chat']['username']
    res = cursor.execute("SELECT * FROM towns WHERE town = '{t}' LIMIT 1".format(t=town.upper())).fetchone()
    if res:  # Got input
        if res[1] == 0:  # Town was not used
            res2 = cursor.execute("SELECT * FROM users WHERE username = '{u}' LIMIT 1".format(u=username)).fetchone()
            if res2:  # User found! Continue gaming
                if town[0] != res2[2]:
                    update.message.reply_text(
                        'My last answer was ' + res2[1] + ', your town must begin with letter ' + res2[2])
                    return
                else:
                    res8 = cursor.execute("UPDATE towns SET is_used = 1 WHERE town = '{t}'".format(t=town))
                    conn.commit()
                    my_move(town, username)  # Computer move
                    return
            else:  # New user, welcome
                update.message.reply_text('Welcome, new user')
                res2 = cursor.execute("INSERT INTO users VALUES ('{u}', '{t}', '')".format(u=username, t=town))
                res5 = cursor.execute("UPDATE towns SET is_used = 1 WHERE town = '{t}'".format(t=town))
                conn.commit()
                update.message.reply_text('Your city: ' + town)
                my_move(town, username)  # Computer move
                return
        else:
            update.message.reply_text('City was already taken')
    else:
        update.message.reply_text('No such city found')


def clear(bot, update, user_data):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    res = cursor.execute("UPDATE towns SET is_used = 0")
    conn.commit()
    update.message.reply_text('All citieas are cleared')


def calculator(bot, update, user_data):
    try:
        update.message.reply_text(eval(update['message']['text'].replace('/calc ', '').replace(' ', '')))
    except:
        update.message.reply_text('Error')


def help(bot, update, user_data):
    text = """Hi, I am a Armornikbot\r\n/calc - Calculator\r\n/c - Town game
    \r\n/clear - clear used cities in towngame"""
    update.message.reply_text(text)
