#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request
from session.session import Browser
from os import environ
import base64
import session
import requests

log = session.Account()
ses = Browser()
app = Flask(__name__)
url = 'https://api.telegram.org/bot' + environ["TOKEN"]




def update(update):
    try:
        message = str(update['message']['text'])
    except:
        message = ''
    if 'new_chat_member' in str(update):
        nama_grup = update['message']['chat']['title']
        grup_id   = update['message']['chat']['id']
        mem_baru  = update['message']['new_chat_member']['first_name']
        teks      = f'Hai {mem_baru} !\nSelamat datang di Grup {nama_grup}'
        kirim_pesan(grup_id, teks)
    elif message.lower().startswith('/about'):
        text = 'Hy, i\'m Smbf bot\nI was made for find random account on facebook\nBut I am still in the development stage\nI was made by t.me/asmindev'
        kirim_pesan(update['message']['chat']['id'], text)
    elif message.startswith('/login'):
        if len(message.split(' ')) != 1:
            ses.setkuki = message.split(' ',1)[1].replace(' ','')
            data = ses.get('/me').text
            text = log.login(data)
            if text:
               kirim_pesan(update['message']['chat']['id'], 'Login successfully')
            else:
                kirim_pesan(update['message']['chat']['id'], 'Login failed!\nCheck your cookie\n' + str(data))
        else:
            kirim_pesan(update['message']['chat']['id'], 'Usage:\n\t/login <your cookie here>')
    else:
        id = update['message']['chat']['id']
        kirim_pesan(id, str(update['message']['text']))
def kirim_pesan(id, teks):
    data = {'chat_id':id,'text':teks}
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

