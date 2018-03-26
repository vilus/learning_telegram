# -*- coding: utf-8 -*-
import logging
from .demultiplexer import get_parser
from .service import HAService
from .api import get_api
from common import cache
from common.tools import get_tools
from common.sender import get_sender


def _build_ha_service(conf):
    logging.debug('creating `HA` weather service')
    fast_cache = cache.get_cache(storage=conf['fast_cache_type'], **conf)
    slow_cache = cache.get_cache(storage=conf['slow_cache_type'], **conf)

    return HAService(conf, get_parser(conf),
                     fast_cache, slow_cache,
                     get_tools(conf),
                     get_sender(conf),
                     get_api(conf))


def get_service(conf):
    builder_map = {
        'ha': _build_ha_service
    }
    service_type = conf['weather_service_type']
    return builder_map[service_type](conf)
