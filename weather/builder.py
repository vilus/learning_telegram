# -*- coding: utf-8 -*-
import parser
from .service import HAService
from .api import get_api
# TODO: need to think about hard '..'
from ..common import cache
from ..common import tools as tls


def _build_ha_service(conf):
    fast_cache = cache.get_cache(storage=conf['fast_cache_type'], **conf)
    slow_cache = cache.get_cache(storage=conf['slow_cache_type'], **conf)

    tools = tls.get_tools(conf)

    import mock
    sender = mock.Mock()  # TODO: implement
    ext_api = get_api(conf)

    return HAService(conf, parser, fast_cache, slow_cache, tools, sender, ext_api)


def build_service(conf):
    builder_map = {
        'ha': _build_ha_service
    }
    service_type = conf['weather_service_type']
    return builder_map[service_type](conf)
