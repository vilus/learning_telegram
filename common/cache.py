# -*- coding: utf-8 -*-
import beaker.cache as cache


def get_cache_in_memory(**_):
    """
    memory
    """
    return cache.Cache('im_memory', type='memory')


def get_cache_in_db(**params):
    """
    params:
        - cache_name: optional
        - db_url
    ext:database
    """
    return cache.Cache(params.get('cache_name', 'cache_in_db'), url=params['db_url'], type='ext:database')


def get_cache_in_redis(**params):
    """
    ext:redis
    """
    raise NotImplementedError


def get_cache(storage='memory', **params):
    createfunc_map = {
        'memory': get_cache_in_memory,
        'db': get_cache_in_db,
        'redis': get_cache_in_redis
    }
    return createfunc_map[storage](**params)
