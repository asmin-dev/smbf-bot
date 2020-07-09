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
    try:
        if data['text'].startswith('/start'):
            '''
        {'update_id': 252837133, 'message': {'message_id': 988, 'from': {'id': 932559405, 'is_bot': False, 'first_name': 'asmin', 'username': 'asmindev', 'language_code': 'id'}, 'chat': {'id': 932559405, 'first_name': 'asmin', 'username': 'asmindev', 'type': 'private'}, 'date': 1593951913, 'text': '/start', 'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}}
            '''
            mem_baru  = update['message']['first_name']
            teks      = f'Hai {mem_baru} !\n now you here'
            send(data['id'],teks)
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
        elif data['text'].lower.startswith('/list'):
            if not Ses.logged:
                send(data['id'], 'You must login!')
            else:
                send(data['id'], 'Please wait, getting user')
                link = session.parsing.parsing(ses.get('/me').content).find_all('a',string="Teman")
                for url in link:
                    if 'friends/center' in str(url):
                        continue
                    else:
                        id= user.friendlist(url['href'])
                        send(data['id'], id)
        else:
            send(data['id'], data['text'])
    except Exception as f:
        send(data['id'], str(f))
def send(id, teks):
    data = {'chat_id':id,'text': str(teks)}
    requests.get(url  + '/sendMessage', params=data)

@app.route('/',methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data_update = request.get_json()
        update(data_update)
        return 'oke'
    else:
        return 'NOTHING FOUND HERE'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(environ.get('PORT', '5000')), debug=True)

