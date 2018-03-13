# -*- coding: utf-8 -*-
from weather_mediator import tell_weather


def weather(bot, update):
    """
    Hard dependency to cmd /say
    background task must applied its results via: back_data["message"]["text"].format(res)
    TODO: recreate above hard solution (as first compromise, extract to separate method back_data and the weather)
    :param bot:
    :param update:
    :return:
    """
    update.message.text = "/say >> weather: {0}"
    back_data = update.to_dict()
    # tasks.weather.delay(back_data)
    tell_weather(back_data)
