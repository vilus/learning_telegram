# -*- coding: utf-8 -*-
import time
from mock import Mock
from ..tools import get_tools, make_db_url


def test_get_weather_location():
    pass


def test_increase_value():
    t = get_tools({'db_url': 'sqlite:///', 'db_echo': True})
    count, _ = t.increase_counter('test_increase_value', ttl=1)
    assert count == 1
    count, _ = t.increase_counter('test_increase_value', ttl=1)
    assert count == 2
    count, _ = t.increase_counter('test_increase_value', ttl=2)
    assert count == 3
    time.sleep(1)
    count, _ = t.increase_counter('test_increase_value', ttl=2)
    assert count == 2


def test_decrease_value():
    t = get_tools({'db_url': 'sqlite:///', 'db_echo': False})
    count, c_id1 = t.increase_counter('test_decrease_value', ttl=2)
    assert count == 1
    count, c_id2 = t.increase_counter('test_decrease_value', ttl=2)
    assert count == 2

    t.decrease_counter(c_id2)
    count, c_id = t.increase_counter('test_decrease_value', ttl=2)
    assert count == 2
    t.decrease_counter(c_id1)
    count, c_id = t.increase_counter('test_decrease_value', ttl=2)
    assert count == 2

    count, c_id = t.increase_counter('test_decrease_value', ttl=2)
    t.decrease_counter(100500)
    assert count == 3


def test_incr_decr_value():
    t = get_tools({'db_url': 'sqlite:///', 'db_echo': False})
    with t.incr_decr('test_incr_decr_value', ttl=2) as count:
        assert count == 1
    with t.incr_decr('test_incr_decr_value', ttl=2) as count:
        assert count == 1

    t.increase_counter('test_incr_decr_value', ttl=2)
    with t.incr_decr('test_incr_decr_value', ttl=2) as count:
        assert count == 2
    count, _ = t.increase_counter('test_incr_decr_value', ttl=2)
    assert count == 2


def test_wait():
    t = get_tools({'db_url': 'sqlite:///', 'db_echo': False})
    assert t.wait(lambda: True, timeout=5)
    assert not t.wait(lambda: False, timeout=2)

    mock = Mock()
    mock.side_effect = (None, None, True, None)
    assert t.wait(mock, timeout=600)
    assert mock.call_count == 3


# TODO: make fixture for get_tools
def test_is_allowed_service():
    t = get_tools({'db_url': 'sqlite:///', 'db_echo': False})
    # t = get_tools({'db_url': 'postgres://postgres@192.168.99.101:5432/postgres', 'db_echo': False})
    assert t.is_allowed_service('test_is_allowed_service', rate=1)
    assert not t.is_allowed_service('test_is_allowed_service', rate=1)

    time.sleep(1)
    assert t.is_allowed_service('test_is_allowed_service', rate=1)

    time.sleep(1)
    assert not t.is_allowed_service('test_is_allowed_service', rate=0.5)
    assert not t.is_allowed_service('test_is_allowed_service', rate=0.5)
    time.sleep(1)
    assert t.is_allowed_service('test_is_allowed_service', rate=0.5)

    time.sleep(1)
    assert t.is_allowed_service('test_is_allowed_service', rate=1)


def test_make_db_url():
    assert 'sqlite:///' == make_db_url({'db_url': 'sqlite:///'})
    conf = dict(db_drivername='postgres', db_user='username',
                db_name='db_name', db_password='psswd',
                db_host='127.0.0.1', db_port=5432)
    assert 'postgres://username:psswd@127.0.0.1:5432/db_name' == make_db_url(conf)
