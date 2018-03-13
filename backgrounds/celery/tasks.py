# -*- coding: utf-8 -*-
from os import environ
from requests import post
from .celery import app


back_api = environ.get('back_api', 'http://127.0.0.1:8080/incoming')


@app.task
def weather(back_data):
    import time
    time.sleep(2)
    back_data['message']['text'] = back_data['message']['text'].format('+40 epta')
    send_say_cmd(back_data)


@app.task
def send_say_cmd(back_data):
    post(back_api, json=back_data)
