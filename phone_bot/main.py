import telebot
from telebot.types import Message
import config
from telebot import types
import requests
import json
import sqlite3
import online_sms_api as sms_api
from threading import Thread
import re
threads=[]
client = telebot.TeleBot(config.CONFIG['token'])

'''def update():
    while True:
        db = sqlite3.connect('users.db')
        cursor = db.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id TEXT,
            user_language TEXT,
            number_one TEXT,
            number_two TEXT,
            country
            
        )""")

        for i in cursor.execute("SELECT number_one FROM users"):
            number = i[0]
            
        
'''


def lang(text: str, lang: str) -> str:
    #print(lang, text)
    with open('languages.json', 'r', encoding='UTF-8') as f:
        data = json.loads(f.read())
    
    try:
        return data[lang][text]
    except KeyError:
        try:
            return data['en'][text]
        except:
            return 'Text not found'

def countries(lang: str, text: str) -> str:
    #print(lang, text)
    #try:
    with open(f'countries_{lang}.json', 'r', encoding='UTF-8') as f:
        data = json.loads(f.read())
    #except:
    #    return 'Lang not found'
    
    
    return data[text.upper()]
    


def main(message):
    db = sqlite3.connect('users.db')
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id TEXT,
        user_language TEXT,
        number_one TEXT,
        number_two TEXT,
        country TEXT,
        number_id TEXT
        
    )""")

    markup_inline = types.InlineKeyboardMarkup()
    
    
    
    
    
    

    for i in cursor.execute(f"SELECT user_language FROM users WHERE user_id = '{message.chat.id}'"):
        user_lang = i[0]
    countrys = types.InlineKeyboardButton(lang("countrys", user_lang), callback_data='countrys')
    markup_inline.add(countrys)

    client.send_message(message.chat.id, lang('main', user_lang), reply_markup=markup_inline)



@client.message_handler(commands=['start'])
def welcom(message):
    db = sqlite3.connect('users.db')
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id TEXT,
        user_language TEXT,
        number_one TEXT,
        number_two TEXT,
        country TEXT,
        number_id TEXT
        
    )""")
        


    db.commit()
    cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{message.chat.id}'")
    
    if cursor.fetchone() is None:
        users_list = [message.chat.id, message.from_user.language_code, 'None', 'None', 'us', 'None']

        cursor.execute("INSERT INTO users VALUES(?,?,?,?,?,?);", users_list)
    
    db.commit()
    

    #print(message.from_user.language_code)
    msg = lang('start_message', message.from_user.language_code)

    print(msg)


    


    markup_inline = types.InlineKeyboardMarkup()

    ru = types.InlineKeyboardButton('Русский', callback_data='ru')
    en = types.InlineKeyboardButton('English', callback_data='en')
    markup_inline.add(ru, en)
    client.send_message(message.chat.id, msg, reply_markup=markup_inline)

@client.message_handler(commands=['main'])
def main_command(message):
    main(message)


def select2(message):
    
    db = sqlite3.connect('users.db')
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id TEXT,
        user_language TEXT,
        number_one TEXT,
        number_two TEXT,
        country TEXT,
        number_id TEXT
        
    )""")
        

    for i in cursor.execute(f"SELECT country FROM users WHERE user_id = '{message.chat.id}'"):
        l = i[0]
    print(l)
    for i in cursor.execute(f"SELECT user_language FROM users WHERE user_id = '{message.chat.id}'"):
        user_lang = i[0]
    if lang('big_numbers', user_lang) in message.text:
        numbers = sms_api.get_numbers(l)
        
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)

        for number in numbers:
            button = types.KeyboardButton(numbers['data'][number]['number'])

            markup_reply.add(button)
        for i in cursor.execute(f"SELECT user_language FROM users WHERE user_id = '{message.chat.id}'"):
            user_lang = i[0]
        msg = client.send_message(message.chat.id, lang('select_numbes', user_lang), reply_markup=markup_reply)
        client.register_next_step_handler(msg, select2)
    else:
        cursor.execute(f"UPDATE users SET number_one = '{message.text}' WHERE user_id = '{message.chat.id}'")
        db.commit()
        markup = types.ReplyKeyboardRemove()
        client.send_message(message.chat.id, lang('little', user_lang), reply_markup=markup)








def select(message):
    db = sqlite3.connect('users.db')
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id TEXT,
        user_language TEXT,
        number_one TEXT,
        number_two TEXT,
        country TEXT,
        number_id TEXT
        
    )""")
    db.commit()
    
    for i in cursor.execute(f"SELECT country FROM users WHERE user_id = '{message.chat.id}'"):
        country = i[0]
    if '!' in message.text:
        text = re.search(r'\w+', message.text)
        print(text)



    
    numbers = sms_api.get_numbers(country)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(numbers, f, ensure_ascii=False, indent=4)
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for number in range(0, 5):
        print(numbers['data'][number]['number'])
        button = types.KeyboardButton(numbers['data'][number]['number']) 

        markup_reply.add(button)
    for i in cursor.execute(f"SELECT user_language FROM users WHERE user_id = '{message.chat.id}' "):
        user_lang = i[0]
    big = types.KeyboardButton(lang('big_numbers', user_lang))
    markup_reply.add(big)

    client.send_message(message.chat.id, lang('select_numbers', user_lang), reply_markup=markup_reply)
    cursor.execute(f"UPDATE users SET country = '{text}' WHERE user_id = '{message.chat.id}'")
    db.commit()
    
    client.register_next_step_handler(message, select2)


    
    


    
        




@client.callback_query_handler(func=lambda call: True)
def answer(call):
    db = sqlite3.connect('users.db')
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id TEXT,
        user_language TEXT,
        number_one TEXT,
        number_two TEXT,
        country TEXT,
        number_id TEXT
        
    )""")
        

    
    


    
        
    if call.data == 'ru':
        
        cursor.execute(f"UPDATE users SET user_language = 'ru' WHERE user_id = '{call.message.chat.id}'")
        db.commit()


        client.delete_message(call.message.chat.id, call.message.message_id)
        main(call.message)

    elif call.data == 'en':
        
        cursor.execute(f"UPDATE users SET user_language = 'en' WHERE user_id = '{call.message.chat.id}'")
        db.commit()
        client.delete_message(call.message.chat.id, call.message.message_id)
        main(call.message)

    elif call.data == 'countrys':
        for i in cursor.execute(f"SELECT user_language FROM users WHERE user_id = '{call.message.chat.id}'"):
            user_lang = i[0]
        client.delete_message(call.message.chat.id, call.message.message_id)
        countrys = sms_api.get_countries()['data']

        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)

        for country2 in countrys:
            button = types.KeyboardButton(countries(user_lang, country2['country']) + ' !' + country2['country'])
            markup_reply.add(button)
        
        
            
            
            

        
        


        client.send_message(call.message.chat.id, lang("select_countrys_text", user_lang), reply_markup=markup_reply)
        client.register_next_step_handler(call.message, select)






        
'''thread1=Thread(target=update); threads.append(thread1)
for t in threads:
    t.start()
'''


client.polling(none_stop=True, interval=0)



