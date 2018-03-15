# -*- coding: utf-8 -*-


class MockWeatherApi:
    def get_weather(self, location):
        return '+28'


def get_api(conf):
    """
    :param wheather_service: openweathermap.org or worldweatheronline.com or else
    """
    return MockWeatherApi()
