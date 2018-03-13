# -*- coding: utf-8 -*-
import abc


class ChainHandler:
    metaclass = abc.ABCMeta

    def __init__(self, successor=None):
        self._successor = successor

    @abc.abstractmethod
    def handle_request(self, *_, **__):
        pass


class SendReplyHandler(ChainHandler):
    def handle_request(self, config, **_):
        pass


class FromFastCacheHandler(ChainHandler):
    def handle_request(self, config, **_):
        pass


class FromPersistentCacheHandler(ChainHandler):
    def handle_request(self, config, **_):
        pass


class WeatherServiceHandler(ChainHandler):
    def handle_request(self, config, **_):
        pass

'''
class ToFastCacheHandler(ChainHandler):
    def handle_request(self, config, **_):
        pass


class ToPersistentCacheHandler(ChainHandler):
    def handle_request(self, config, **_):
        pass
'''

if __name__ == '__main__':
    print('ok')
