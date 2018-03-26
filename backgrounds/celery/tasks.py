# -*- coding: utf-8 -*-
from uuid import uuid4
from .celery import app


@app.task
def say_weather(conf, back_data):
    from weather import builder
    service = builder.get_service(conf)
    return service.handle(back_data, str(uuid4()))


def run(cmd, conf, params):
    cmd_map = {
        'say_weather': say_weather,
    }
    return cmd_map[cmd].delay(conf, params)
