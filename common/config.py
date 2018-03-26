# -*- coding: utf-8 -*-
import logging
from os import environ


"""
Getting configuration (as dict) from several sources.
Source must be set via environment variable "CONFIG_SRC",
otherwise as source will be used "ini" file (i.e. by default)
Available sources:
- "env" (variables must have prefix PREFIX (see below), as example "TLM_WEATHER_SYTI")
- "ini"
- "db" (DB_HOST, DB_USER, DB_NAME are passed also via environ)
For example:
# export CONFIG_SRC="env"
"""


PREFIX = environ.get('CONFIG_PREFIX', 'TLM_')


def from_env():
    logging.debug('creating conf from env')
    conf = dict((k.lstrip(PREFIX).lower(), v) for k, v in environ.items() if k.startswith(PREFIX))
    return conf


def from_ini():
    logging.debug('creating conf from ini')
    # TODO: to implement
    raise NotImplementedError


def from_db():
    logging.debug('creating conf from db')
    # TODO: to implement
    raise NotImplementedError


def get_conf(src='ini'):
    source_mapping = {
        'env': from_env,
        'ini': from_ini,
        'db': from_db,
    }
    config_src = environ.get(PREFIX+'CONFIG_SRC', src)
    conf = source_mapping[config_src]()
    logging.debug('created conf: {0}'.format(conf))
    return conf
