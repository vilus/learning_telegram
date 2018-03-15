# -*- coding: utf-8 -*-
import logging

TASK_TIMEOUT = 60
WEATHER_CACHE_TIMEOUT = 4*60*60
WEATHER_API_RATE = 1/(60*60)


class HAService:
    def __init__(self, conf, parser, fast_cache, slow_cache, tools, sender, ext_api):
        self.conf = conf
        self.parser = parser
        self.fast_cache = fast_cache
        self.slow_cache = slow_cache
        self.sender = sender    #
        self.tools = tools      #
        self.ext_api = ext_api
        self.task_timeout = self.conf.get('task_running_timeout', TASK_TIMEOUT)  # TODO: rename
        self.check_interval = self.conf.get('check_task_interval', 1)
        self.cache_timeout = self.conf.get('weather_cache_timeout', WEATHER_CACHE_TIMEOUT)
        self.api_rate_limit = self.conf.get('weather_api_rate', WEATHER_API_RATE)

    def handle(self, back_data, req_id):
        # validation params
        # get from fast cache
        #     create answer and send result
        #     return
        # register task
        #     check slow cache
        #         update fast cache
        #         un_register task
        #         create answer and send result
        #         return
        #     allowed external api
        #         use external api
        #         update fast cache
        #         update slow cache
        #         un_register task
        #         create answer and send result
        #         return
        # wait (i.e. other task already running now)
        # get from fast cache
        #     create answer and send result
        # return

        logging.debug('start handling request: {0}'.format(req_id))

        self.parser.check_params(back_data)
        location = self.parser.get_weather_location(back_data)
        weather = self.get_weather(location, req_id)
        self.sender.reply(back_data, weather)

    # TODO: rewrite usage of fast and slow cache via class method decorator
    def get_weather(self, location, req_id):
        """
        :return:
        """
        # TODO: rewrite 'in' to 'get' and check on None !!!
        if location in self.fast_cache:
            # race condition !
            return self.fast_cache.get(location)

        res = 'The weather temporary unavailable, pls try later'
        running_task, counter_id = self.tools.increase_counter(location, self.task_timeout)
        if running_task > 1:
            # already running getting weather by location from slow cache or external api
            self.tools.decrease_counter(counter_id)
            if self.tools.wait(lambda: location in self.fast_cache, self.task_timeout, self.check_interval):
                res = self.fast_cache.get(location)
            return res

        if location in self.slow_cache:
            res = self.slow_cache.get(location)
            self.fast_cache.set_value(location, res, expiretime=self.cache_timeout)
            self.tools.decrease_counter(counter_id)
            return res

        if self.tools.is_allowed_service(self.ext_api, self.api_rate_limit):
            try:
                res = self.ext_api.get_weather(location)
            except Exception as e:
                logging.error('req_id: {0}, got error {1} when getting the weather from api'.format(req_id, e))
            else:
                self.fast_cache.set_value(location, res, expiretime=self.cache_timeout)
                self.slow_cache.set_value(location, res, expiretime=self.cache_timeout)

        self.tools.decrease_counter(counter_id)
        return res


class SimpleService:
    def handle(self):
        pass


class MockService:
    def handle(self):
        pass

'''
def get_service(tag=''):
    """return just cls! not created object"""
    service_map = {
        'ha': HAService,
        'simple': SimpleService,
        'mock': MockService,
    }
    return service_map[tag]
'''