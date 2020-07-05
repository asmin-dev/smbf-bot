#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request
from session.session import Browser
from lib import Main
from os import environ

import session
import requests

user = Main()
Ses = session.Account()
ses = Browser()
app = Flask(__name__)
url = 'https://api.telegram.org/bot' + environ["TOKEN"]


def messages(data):
    try:
        text = str(data['message']['text'])
        id = data['message']['chat']['id']
        return {'text':text, 'id':id}
    except:
        return None

def update(update):
    data = messages(update)
    if 'new_chat_member' in str(update):
        nama_grup = update['message']['chat']['title']
        grup_id   = update['message']['chat']['id']
        mem_baru  = update['message']['new_chat_member']['first_name']
        teks      = f'Hai {mem_baru} !\nSelamat datang di Grup {nama_grup}'
        send(grup_id, teks)
    elif data['text'].lower().startswith('/about'):
        text = 'Hy, i\'m Smbf bot\nI was made for find random account on facebook\nBut I am still in the development stage\nI was made by t.me/asmindev'
        send(data['id'], text)
    elif data['text'].startswith('/login'):
        if len(data['text'].split(' ')) != 1:
            ses.setkuki = data['text'].split(' ',1)[1].replace(' ','')
            if Ses.login(ses):
                send(data['id'], 'Login successfully')
                user.browser = ses
            else:
                send(data['id'], 'Login failed!\nCheck your cookie')
        else:
            send(data['id'], 'Usage:\n/login <your cookie here>')
    elif data['text'].startswith('/myinfo'):
        if not Ses.logged:
            send(data['id'], 'You must login')
        else:
            send(data['id'], Ses.__str__(ses))
    elif data['text'].startswith('/list'):
        if not Ses.logged:
            send(data['id'], 'You must login!')
        else:
            send(data['id'], 'Please wait, getting user')
            link = session.parsing.parsing(ses.get('/me').content).find_all('a',string="Teman")
            for url in link:
                if 'friends/center' in str(url):
                    continue
                else:
                    data = user.friendlist(url['href'])
                    print(data)
                    print(type(data))
                    send(data['id'], str(data))
    else:
        send(data['id'], data['text'])
def send(id, teks):
    data = {'chat_id':id,'text':str(teks)}
    requests.get(url  + '/sendMessage', params=data)

@app.route('/',methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data_update = request.get_json()
        update(data_update)
        return "oke"
    else:
        return 'NOTHING FOUND HERE'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(environ.get('PORT', '5000')), debug=True)

