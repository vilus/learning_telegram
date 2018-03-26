# -*- coding: utf-8 -*-
from jsonschema import validate


class ParseError(Exception):
    pass


def get_weather_location(params):
    """by default parse json telegram msg"""
    return params["message"]["text"].split()[1]


# simplistically
default_tlm_schema = {
    'type': 'object',
    'properties': {
        'update_id': {'type': 'integer'},
        'message': {
            'type': 'object',
            'properties': {
                'message_id': {'type': 'integer'},
                'date': {'type': 'integer'},
                'text': {'type': 'string'},
                'from': {'type': 'object'},
                'chat': {'type': 'object'},
            },
            'required': ['message_id', 'date', 'text', 'from', 'chat']
        },
    },
    'required': ['update_id', 'message']
}


def check_params(params):
    """by default params is json from telegram server msg"""
    validate(params, default_tlm_schema)
    # check format of inner message
    msg = params["message"]["text"]
    if '{0}' not in msg:
        raise ParseError('"{0}" not found in message.text')
    # expected format: "/some_cmd weather_location weather: {0}"
    if len(msg.split()) < 4:
        raise ParseError('message.text too short')


def get_parser(_):
    # TODO: refactor
    import sys
    return sys.modules[__name__]
