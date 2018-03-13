# -*- coding: utf-8 -*-
import pytest
from ..parser import get_weather_location, check_params


def test_get_weather_location():
    params = {'message': {'text': '/say Bangkok weather: {0}'}}
    assert get_weather_location(params) == 'Bangkok'


def test_check_params():
    params = {
        'update_id': 1,
        'message': {
            'message_id': 100500,
            'date': 1516121407,
            'text': '/say Bangkok weather: {0}',
            'from': {},
            'chat': {},
        }
    }
    check_params(params)
    with pytest.raises(Exception):
        params['message']['text'] = '/say Bangkok weather: ololo'
        check_params(params)
    with pytest.raises(Exception):
        params['message']['text'] = 'Hi'
        check_params(params)
