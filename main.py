# -*- coding: utf-8 -*-
import logging
import os
import telegram
import sys
from flask import Flask, request
from handlers import get_dispatcher


TOKEN = os.environ.get('token')
HOOK = os.environ.get('hook', '/incoming')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

app = Flask(__name__)
app.debug = True
bot = telegram.Bot(token=TOKEN)


@app.route(HOOK, methods=['POST'])  # TODO: replace HOOK to HOOK + TOKEN
def webhook_handler():
    data = request.get_json(force=True)
    logging.debug('incoming data: {0}'.format(data))
    update = telegram.Update.de_json(data, bot)
    dp = get_dispatcher(bot)
    dp.process_update(update)
    return ''


@app.route('/')
def index():
    return 'Hello World'


sys.path.append('.')
sys.path.append('..')  # ^(
sys.path.append('...')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
