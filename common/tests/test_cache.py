# -*- coding: utf-8 -*-
import time
import pytest
from ..cache import get_cache


@pytest.fixture(params=[{'storage': 'memory'}, {'storage': 'db', 'db_url': 'sqlite:///'}],
                ids=['in_memory', 'in_db'])
def cache(request):
    c = get_cache(**request.param)
    c.set_value('test', 42, expiretime=1)
    return c


def test_get(cache):
    assert cache.get('test') == 42


def test_in(cache):
    assert 'test' in cache
    assert 'ololo' not in cache


def test_expired(cache):
    time.sleep(1)
    assert not cache.has_key('test')
