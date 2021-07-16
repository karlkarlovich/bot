import sqlite3 as sql
import random

import config
import bot_algs

from aiogram import Bot, Dispatcher, executor, types

db=sql.connect('bot.db')
cursor=db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INT
)""")

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
user_id=0

@dp.message_handler(commands=['start'])
async def start(message):
    sti=open('sticker.webp','rb')
    await bot.send_sticker(message.chat.id,sti)
    await bot.send_message(message.chat.id,"Привет {0.first_name}, я {1.first_name}!".format(message.from_user, bot.get_me()),parse_mode='html')

    sdb=sql.connect('bot.db')
    scursor=sdb.cursor()
    scursor.execute(f"SELECT id FROM users WHERE id='{message.from_user.id}'")
    if scursor.fetchone()==None:
        scursor.execute("INSERT INTO users VALUES (?)",(message.from_user.id,))
        sdb.commit()


@dp.message_handler(content_types=['text'])
async def lalala(message):
    mdb=sql.connect('bot.db')
    mcursor=mdb.cursor()

    if(message.chat.id!=config.admin_chat_id):
        await bot.send_message(config.admin_chat_id ,message.chat.id)
        await bot.send_message(config.admin_chat_id ,"{0.first_name}  {0.last_name} :".format(message.from_user, bot.get_me()),parse_mode='html')
        await bot.send_message(config.admin_chat_id ,message.text)
        print("{0.first_name} {0.last_name}:".format(message.from_user, bot.get_me()),message.text,"(",message.chat.id,")")

    if message.text=="send message" and message.chat.id==config.admin_chat_id:
        print("sending message")
        await bot.send_message(message.chat.id,"введи текст сообщения")
        #bot.register_next_step_handler(message, sending_message)
    elif message.text=="check db" and message.chat.id==config.admin_chat_id:
        for i in mcursor.execute("SELECT * FROM users"):
            a=str(i[0])+"---"+str(i[1])
            await bot.send_message(config.admin_chat_id,a)

    else:
        await bot_algs.mhandler(message,mdb,mcursor,bot)

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



if __name__ =='__main__':
    executor.start_polling(dp, skip_updates=False)
