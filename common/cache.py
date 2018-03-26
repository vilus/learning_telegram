# -*- coding: utf-8 -*-
import logging
import beaker.cache as cache
from .tools import make_db_url


class CustomCache(cache.Cache):
    def get(self, key, default=None):
        try:
            return super(CustomCache, self).get(key)
        except KeyError:
            return default


def get_cache_in_memory(**_):
    """
    memory
    """
    logging.debug('creating beaker cache in memory')
    return CustomCache('im_memory', type='memory')


def get_cache_in_db(**params):
    """
    params:
        - cache_name: optional
        - db_url
    ext:database
    """
    cache_db_prefix = params.get('cache_db_prefix', '')
    db_url = make_db_url(params, cache_db_prefix)
    logging.debug('creating beaker cache in db {0}'.format(db_url))
    return CustomCache(params.get('db_cache_name', 'cache_in_db'),
                       url=db_url,
                       type='ext:database')


def get_cache_in_redis(**params):
    """
    ext:redis
    """
    redis_url = params['redis_url']
    logging.debug('creating beaker cache in redis in {0}'.format(redis_url))
    ns = params.get('redis_cache_name', 'cache_in_redis')
    return CustomCache(ns, url=redis_url, type='ext:redis')


def get_cache(storage='memory', **params):
    createfunc_map = {
        'memory': get_cache_in_memory,
        'db': get_cache_in_db,
        'redis': get_cache_in_redis
    }
    return createfunc_map[storage](**params)
