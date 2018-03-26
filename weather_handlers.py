# -*- coding: utf-8 -*-
from backgrounds import get_background
from common import config


def weather(_, update):
    """
    Hard dependency to cmd /say
    background task must applied its results via: back_data["message"]["text"].format(res)
    TODO: recreate above hard solution (as first compromise, extract to separate method back_data and the weather)
    :param _: bot
    :param update:
    :return:
    """
    update.message.text = "/say Voronezh,RU weather: {0}"
    back_data = update.to_dict()
    conf = config.get_conf()
    bg = get_background(conf)
    bg.run('say_weather', conf, back_data)
