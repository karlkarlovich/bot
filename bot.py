import sqlite3 as sql
import random

import config
import bot_algs

from aiogram import Bot, Dispatcher, executor, types

db = sql.connect('bot.db')
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INT
)""")

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message):
    sti = open('hello.webp', 'rb')
    await bot.send_sticker(message.chat.id, sti)
    me = await bot.get_me()
    msg = f"Привет {message.from_user.first_name}, я {me.first_name}!"
    await bot.send_message(message.chat.id, msg)

    sdb = sql.connect('bot.db')
    scursor = sdb.cursor()
    scursor.execute(f"SELECT id FROM users WHERE id='{message.from_user.id}'")
    if scursor.fetchone() is None:
        scursor.execute(
            "INSERT INTO users VALUES (?)", (message.from_user.id,))
        sdb.commit()


@dp.message_handler(content_types=['text'])
async def lalala(message):
    mdb = sql.connect('bot.db')
    mcursor = mdb.cursor()

    if(message.chat.id != config.admin_chat_id):
        for_admin = f"""
{message.from_user.first_name} {message.from_user.last_name}
({message.chat.id}): {message.text}
        """
        await bot.send_message(config.admin_chat_id, for_admin)
        print(for_admin)

    if message.chat.id == config.admin_chat_id:
        if message.text == "send message":
            print("sending message")
            await bot.send_message(message.chat.id, "введи текст сообщения")
            # bot.register_next_step_handler(message, sending_message)
        elif message.text == "check db":
            for i in mcursor.execute("SELECT * FROM users"):
                a = f"{i[0]}---{i[1]}"
                await bot.send_message(config.admin_chat_id, a)
        else:
            await bot_algs.mhandler(message, mdb, mcursor, bot)
    else:
        await bot_algs.mhandler(message, mdb, mcursor, bot)


def sending_message(message):
    atext = message.text
    print("text asked")
    msg = "введи id пользователя, которому ты хочешь написать от моего имени"
    bot.send_message(message.chat.id, msg)
    print("asking id")
    bot.register_next_step_handler(message, atext, ask_id)


def ask_id(message, atext):
    bot.send_message(message.text, atext)
    bot.send_message(message.chat.id, "отправленно")
    print("message sent for", message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
