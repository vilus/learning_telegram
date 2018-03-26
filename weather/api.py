# -*- coding: utf-8 -*-
import logging
import pyowm
from abc import ABC, abstractmethod


class BaseWeatherApi(ABC):
    def __init__(self, conf):
        self.conf = conf

    @property
    @abstractmethod
    def name(self):
        """"""

    @abstractmethod
    def get_weather(self, location):
        """"""


class MockWeatherApi(BaseWeatherApi):
    @property
    def name(self):
        return 'weather_api_mock'

    def get_weather(self, _):
        import time
        time.sleep(15)
        return '+28'


class OpenWeatherMapApi(BaseWeatherApi):
    @property
    def name(self):
        return 'openweathermap_api'

    def get_weather(self, location):
        owm = pyowm.OWM(self.conf['weather_api_token'])
        obs = owm.weather_at_place(location)
        w = obs.get_weather()
        logging.debug('got weather: {0}'.format(w))
        res = '{0} °С, {1}'.format(w.get_temperature('celsius').get('temp'),
                                   w.get_detailed_status())
        return res


def get_api(conf):
    apis_map = {
        'mock': MockWeatherApi,
        'openweathermap': OpenWeatherMapApi,
    }
    api_type = conf['weather_api_type']
    logging.debug('creating weather_api: {0}'.format(api_type))
    return apis_map[api_type](conf)
