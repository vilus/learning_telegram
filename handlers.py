# -*- coding: utf-8 -*-
from telegram.ext import Dispatcher
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='Hi')


def echo(bot, update, args=None):
    if not args:
        args = update.message.text
    else:
        args = ' '.join(args)
    bot.sendMessage(chat_id=update.message.chat_id, text=args)


def get_dispatcher(bot):
    dp = Dispatcher(bot, None, workers=0)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('say', echo, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.command, echo))  # TODO: handle unknown command
    return dp
