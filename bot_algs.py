import dictionary
import random as rand
import requests

import config

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from bs4 import BeautifulSoup as bs

def CTWL (text, key_word_list):#CTWL-check text with list
    flag=False
    for i in key_word_list :
        if fuzz.partial_ratio(i, text)>=70 and len(text)>=len(i)-3:
            flag=True
    return flag


def find_anwser(mtext):
    answers=[]


    for i in dictionary.dict:
        if CTWL(mtext, i.keywords):
            answers = i.answers
            break

    if answers != []:
        answer = answers[rand.randint(0,len(answers)-1)]
    else:
        resaults = searX(mtext)
        answer = "Не понял юмора, поэтому обратился к google~st3|Вот что он сказал:~nn"
        for resault in resaults:
            answer = answer + f"[{resault['title']}]({resault['link']})~md)"

    return answer

async def msender(mtext,bot,id):

    POT = mtext.find("~")
    while POT!=-1:#POT-place of teg

        teg=mtext[slice(POT+1,POT+3)]

        if teg=="nn":
            await bot.send_message(id,mtext[slice(0,POT)])
            mtext=mtext[slice(POT+3,len(mtext))]
        elif teg=="st":
            POE=mtext.find("|")#POE-place of end
            stinum=int(mtext[slice(POT+3,POE)])-1
            await bot.send_message(id,mtext[slice(0,POT)])
            mtext=mtext[slice(POE+1,len(mtext))]
            await bot.send_sticker(id,open(dictionary.stickers[stinum],'rb'))
        elif teg=="md":
            await bot.send_message(id,mtext[slice(0,POT)], parse_mode='Markdown',  disable_web_page_preview = True)
            mtext=mtext[slice(POT+4,len(mtext))]

        POT=mtext.find("~")

    if mtext!='':
        await bot.send_message(id,mtext)


async def mhandler(message,db,cursor,bot):
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id}")
    if cursor.fetchone == None:
        cursor.execute("INSERT INTO users VALUES (?)",(message.from_user.id))
        db.commit()

    mtext=message.text.lower()
    answer=find_anwser(mtext)
    await msender(answer,bot,message.chat.id)


def searX(sear):

    URL = f'https://searx.roughs.ru/search?q={sear}'
    HEADERS = {
        'User-Agent': config.user_agent
    }

    response = requests.get(URL, headers = HEADERS)
    soup = bs(response.content, 'html.parser')
    items = soup.findAll('h4',class_ = 'result_header')
    resaults = []

    for item in items[slice(0,6)]:
        result = item.find('a')

        if result != None:
            resaults.append({
                'title': result.get_text(strip = True),
                'link': result.get('href')
            })

    return resaults
