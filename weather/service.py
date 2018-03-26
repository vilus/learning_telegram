# -*- coding: utf-8 -*-
import logging

TASK_TIMEOUT = 60
WEATHER_CACHE_TIMEOUT = 4*60*60
WEATHER_API_RATE = 1/(60*60)


class HAService:
    # TODO: create abstract base class (handle) and sub-based class (get_weather)
    def __init__(self, conf, parser, fast_cache, slow_cache, tools, sender, ext_api):
        logging.debug('creating HA service of weather')
        self.conf = conf
        self.parser = parser
        self.fast_cache = fast_cache
        self.slow_cache = slow_cache
        self.sender = sender
        self.tools = tools
        self.ext_api = ext_api
        self.task_timeout = float(self.conf.get('task_running_timeout', TASK_TIMEOUT))  # TODO: rename
        self.check_interval = float(self.conf.get('check_task_interval', 1))
        self.cache_timeout = float(self.conf.get('weather_cache_timeout', WEATHER_CACHE_TIMEOUT))
        self.api_rate_limit = float(self.conf.get('weather_api_rate', WEATHER_API_RATE))

    def handle(self, back_data, req_id):
        logging.debug('start handling request: {0}'.format(req_id))

        self.parser.check_params(back_data)
        location = self.parser.get_weather_location(back_data)
        weather = self.get_weather(location, req_id)
        self.sender.reply(back_data, weather)

    def get_weather(self, location, req_id):
        """
        :return:
        """
        res = self.fast_cache.get(location)
        if res:
            return res

        err_msg = 'The weather temporary unavailable, pls try later'

        my_serial_num, c_id = self.tools.increase_counter(location, self.task_timeout)
        if my_serial_num > 1:
            self.tools.decrease_counter(c_id)
            # already running getting weather from slow cache or external api
            res = self.tools.wait(lambda: self.fast_cache.get(location),
                                  self.task_timeout, self.check_interval)
            return res or err_msg

        res = self.slow_cache.get(location)
        if res:
            # TODO: graceful handling cache errors
            self.fast_cache.set_value(location, res, expiretime=self.cache_timeout)
            self.tools.decrease_counter(c_id)
            return res

        if self.tools.is_allowed_service(self.ext_api.name, self.api_rate_limit):
            try:
                res = self.ext_api.get_weather(location)
            except Exception as e:
                # TODO: + traceback
                logging.error('req_id: {0}, got error {1} when '
                              'getting the weather from api'.format(req_id, e))
            else:
                self.fast_cache.set_value(location, res, expiretime=self.cache_timeout)
                self.slow_cache.set_value(location, res, expiretime=self.cache_timeout)
                self.tools.decrease_counter(c_id)
                return res
        self.tools.decrease_counter(c_id)
        return err_msg


class SimpleService:
    def handle(self):
        pass
