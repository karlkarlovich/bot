import dictionary
import random as rand
import requests

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from bs4 import BeautifulSoup as bs

def CTWL (text, key_word_list):#CTWL-check text with list
    flag=False
    for i in key_word_list :
        if fuzz.partial_ratio(i, text)>=70:
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
        resaults = gparse(mtext)
        answer = "Не понял юмора, поэтому обратился к google~st3|Вот что он сказал:~nn"
        for resault in resaults:
            answer = answer + f"[{resault['title']}]({resault['link']})~md)"

    return answer

def msender(mtext,bot,id):

    POT = mtext.find("~")
    while POT!=-1:#POT-place of teg

        teg=mtext[slice(POT+1,POT+3)]

        if teg=="nn":
            bot.send_message(id,mtext[slice(0,POT)])
            mtext=mtext[slice(POT+3,len(mtext))]
        elif teg=="st":
            POE=mtext.find("|")#POE-place of end
            stinum=int(mtext[slice(POT+3,POE)])-1
            bot.send_message(id,mtext[slice(0,POT)])
            mtext=mtext[slice(POE+1,len(mtext))]
            bot.send_sticker(id,open(dictionary.stickers[stinum],'rb'))
        elif teg=="md":
            bot.send_message(id,mtext[slice(0,POT)], parse_mode='Markdown')
            mtext=mtext[slice(POT+4,len(mtext))]

        POT=mtext.find("~")
    bot.send_message(id,mtext)


def mhandler(message,db,cursor,bot):
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id}")
    if cursor.fetchone == None:
        cursor.execute("INSERT INTO users VALUES (?)",(message.from_user.id))
        db.commit()

    mtext=message.text.lower()
    answer=find_anwser(mtext)
    msender(answer,bot,message.chat.id)



def gparse(sear):
    URL = f'http://www.google.ru/search?hl=ru&num=100&q={sear}&start=1'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'
    }

    response = requests.get(URL, headers = HEADERS)
    soup = bs(response.content, 'html.parser')
    items = soup.findAll('div',class_ = 'yuRUbf')
    resaults = []

    for item in items[slice(0,3)]:
        title = item.find('h3', class_ = 'LC20lb DKV0Md')

        if title != None:
            resaults.append({
                'title': title.get_text(strip = True),
                'link': item.find('a').get('href')
            })

    return resaults
