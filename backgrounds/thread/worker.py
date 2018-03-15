# -*- coding: utf-8 -*-
from uuid import uuid4


def say_weather(conf, bach_data):
    from ...weather import builder
    service = builder.build_service(conf)
    return service.handle(bach_data, str(uuid4()))


def run(cmd, conf, **params):
    cmd_map = {
        'say_weather': say_weather,
    }
    return cmd_map[cmd](conf, **params)
