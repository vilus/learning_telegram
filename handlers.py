# -*- coding: utf-8 -*-
from telegram.ext import Dispatcher
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import InlineQueryHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from math_handlers import eval_math_expr
from weather_handlers import weather


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='Hi')


def unknown_cmd(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='Unknown command: {0}'.format(update.message.text))


def echo(bot, update, args=None):
    if not args:
        args = update.message.text
    else:
        args = ' '.join(args)
    bot.sendMessage(chat_id=update.message.chat_id, text=args)


def menu_on(bot, update):
    custom_keyboard = [['/say Hey', '/say Hi'], ['/say Ho', '/say Hyi']]
    #                    top-left   top-right   bottom-left  bottom-right
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    bot.sendMessage(chat_id=update.message.chat_id, text='Menu on', reply_markup=reply_markup)


def menu_off(bot, update):
    reply_markup = ReplyKeyboardRemove()
    bot.sendMessage(chat_id=update.message.chat_id, text="Menu off", reply_markup=reply_markup)


def links(bot, update):
    button_list = [[
        InlineKeyboardButton('bash.im', url='http://bash.im'),
        InlineKeyboardButton('YouTube', url='https://www.youtube.com')
    ]]
    reply_markup = InlineKeyboardMarkup(button_list)
    bot.sendMessage(chat_id=update.message.chat_id, text='Favorite links', reply_markup=reply_markup)


def get_dispatcher(bot):
    dp = Dispatcher(bot, None, workers=0)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('say', echo, pass_args=True))
    dp.add_handler(CommandHandler('menu_on', menu_on))
    dp.add_handler(CommandHandler('menu_off', menu_off))
    dp.add_handler(CommandHandler('links', links))
    dp.add_handler(CommandHandler('weather', weather))
    dp.add_handler(InlineQueryHandler(eval_math_expr))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.command, unknown_cmd))
    return dp
