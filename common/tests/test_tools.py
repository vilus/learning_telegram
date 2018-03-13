# -*- coding: utf-8 -*-
import time
from mock import Mock
from ..tools import get_tools


def test_get_weather_location():
    pass


def test_increase_value():
    t = get_tools({'db_url': 'sqlite:///', 'db_echo': False})
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


def test_wait():
    t = get_tools({'db_url': 'sqlite:///', 'db_echo': False})
    assert t.wait(lambda: True, timeout=5)
    assert not t.wait(lambda: False, timeout=2)

    mock = Mock()
    mock.side_effect = (None, None, True, None)
    assert t.wait(mock, timeout=600)
    assert mock.call_count == 3


def test_is_allowed_service():
    t = get_tools({'db_url': 'sqlite:///', 'db_echo': False})
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
