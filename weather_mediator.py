# -*- coding: utf-8 -*-
from .common.config import get_conf
from .common.background import get_worker


def tell_weather(back_data):
    conf = get_conf()
    worker = get_worker(conf)
    worker.handle('weather', back_data)
