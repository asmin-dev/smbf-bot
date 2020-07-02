#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request
from os import environ
import requests
app = Flask(__name__)
url = 'https://api.telegram.org/bot' + environ["TOKEN"]




def update(update):
    if 'new_chat_member' in str(update):
        nama_grup = update['message']['chat']['title']
        grup_id   = update['message']['chat']['id']
        mem_baru  = update['message']['new_chat_member']['first_name']
        teks      = f'Hai {mem_baru} !\nSelamat datang di Grup {nama_grup}'
        kirim_pesan(grup_id, teks)
    else:
        id = update['message']['chat']['id']
        kirim_pesan(id, str(update['message']['text']))
def kirim_pesan(id, teks):
    data = {
            'chat_id':id,
            'text':teks
            }
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

