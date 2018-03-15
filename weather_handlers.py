# -*- coding: utf-8 -*-
from .backgrounds import get_background
from .common import config


def weather(bot, update):
    """
    Hard dependency to cmd /say
    background task must applied its results via: back_data["message"]["text"].format(res)
    TODO: recreate above hard solution (as first compromise, extract to separate method back_data and the weather)
    :param bot:
    :param update:
    :return:
    """
    update.message.text = "/say Moscow weather: {0}"
    back_data = update.to_dict()
    conf = config.get_conf()
    bg_type = conf.get('bg_type', 'celery')
    bg = get_background(bg_type)
    bg.run('say_weather', conf, back_data)
