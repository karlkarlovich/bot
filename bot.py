import telebot
import sqlite3 as sql
import random

import config
import bot_algs

from telebot import types

db=sql.connect('bot.db')
cursor=db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INT
)""")

bot = telebot.TeleBot(config.TOKEN)
user_id=0

@bot.message_handler(commands=['start'])
def start(message):
    sti=open('sticker.webp','rb')
    bot.send_sticker(message.chat.id,sti)
    bot.send_message(message.chat.id,"Привет {0.first_name}, я {1.first_name}!".format(message.from_user, bot.get_me()),parse_mode='html')

    sdb=sql.connect('bot.db')
    scursor=sdb.cursor()
    scursor.execute(f"SELECT id FROM users WHERE id='{message.from_user.id}'")
    if scursor.fetchone()==None:
        scursor.execute("INSERT INTO users VALUES (?)",(message.from_user.id))
        sdb.commit()


@bot.message_handler(content_types=['text'])
def lalala(message):
    mdb=sql.connect('bot.db')
    mcursor=mdb.cursor()

    if(message.chat.id!=config.admin_chat_id):
        bot.send_message(config.admin_chat_id ,message.chat.id)
        bot.send_message(config.admin_chat_id ,"{0.first_name}  {0.last_name} :".format(message.from_user, bot.get_me()),parse_mode='html')
        bot.send_message(config.admin_chat_id ,message.text)
        print("{0.first_name} {0.last_name}:".format(message.from_user, bot.get_me()),message.text,"(",message.chat.id,")")
    if message.text=="send message" and message.chat.id==config.admin_chat_id:
        print("sending message")
        bot.send_message(message.chat.id,"введи текст сообщения")
        bot.register_next_step_handler(message, sending_message)
    if message.text=="check db" and message.chat.id==config.admin_chat_id:
        for i in mcursor.execute("SELECT * FROM users"):
            a=str(i[0])+"---"+str(i[1])
            bot.send_message(config.admin_chat_id,a)

    else:
        bot_algs.mhandler(message,mdb,mcursor,bot)

def sending_message(message):
    atext=message.text
    print("text asked")
    bot.send_message(message.chat.id,"введи id пользователя, которому ты хочешь написать от моего имени")
    print("asking id")
    bot.register_next_step_handler(message, atext, ask_id)

def ask_id(message,atext):
    bot.send_message(message.text, atext)
    bot.send_message(message.chat.id,"отправленно")
    print("message sent for",message.text)



bot.polling(none_stop=True)
