# -*- coding: utf-8 -*-
import logging
import os
import telegram
from flask import Flask, request


TOKEN = os.environ.get('token')
HOOK = os.environ.get('hook', '/incoming')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

app = Flask(__name__)
app.debug = True
bot = telegram.Bot(token=TOKEN)


@app.route(HOOK, methods=['POST'])
def webhook_handler():
    data = request.get_json(force=True)
    logging.debug('incoming data: {0}'.format(data))
    update = telegram.Update.de_json(data, bot)
    bot.sendMessage(chat_id=update.message.chat.id, text=update.message.text)
    return ''


@app.route('/')
def index():
    return 'Hello World'
