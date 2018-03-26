# -*- coding: utf-8 -*-
from telegram import InlineQueryResultArticle
from telegram import InputTextMessageContent
import simpleeval


simpleeval.MAX_POWER = 1000


def eval_math_expr(bot, update):
    query = update.inline_query.query
    if not query:
        return
    res = 'Failed to calculate'
    try:
        res = simpleeval.simple_eval(query)
    except Exception:
        pass
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Result: {0}'.format(res),
            input_message_content=InputTextMessageContent(res)
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)
