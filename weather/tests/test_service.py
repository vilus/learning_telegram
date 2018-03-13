# -*- coding: utf-8 -*-
from uuid import uuid4
from mock import Mock, MagicMock
from ..service import HAService


class TestHATlmWeatherService:
    """
    Tests of handling request "HA"-algorithm
    """

    def setup(self):
        self.parser = Mock()

        self.conf = Mock()
        conf_values = {'task_running_timeout': 4, 'check_task_interval': 10}
        self.conf.get.side_effect = lambda k, *_, **__: conf_values[k]  # &_&

        self.tools = MagicMock()

        self.fast_cache = MagicMock()
        self.slow_cache = MagicMock()
        self.sender = Mock()
        self.ext_api = Mock()
        # tools, fast_cache, slow_cache, cache_utils, limiter, sender, waiter
        self.target = HAService(conf=self.conf,
                                parser=self.parser,
                                fast_cache=self.fast_cache,
                                slow_cache=self.slow_cache,
                                tools=self.tools,
                                sender=self.sender,
                                ext_api=self.ext_api)
        self.req_id = str(uuid4())

    def test_validation_incoming_params(self):
        self.fast_cache.__contains__.return_value = True
        self.target.handle({}, self.req_id)
        self.parser.check_params.assert_called()

    def test_from_fast_chace(self):
        self.fast_cache.get.return_value = '-16'
        self.fast_cache.__contains__.return_value = True
        self.target.handle({}, self.req_id)
        self.sender.reply.assert_called_with({}, '-16')
        # TODO: check unused slow cache

    def test_already_running_from_slow_or_external(self):
        self.fast_cache.get.return_value = '-11'
        self.fast_cache.__contains__.return_value = False
        # strange, when attr name is 'increase' then return_value is always MagicMock cls
        self.tools.increase_counter.return_value = 2, 1
        self.tools.wait.return_value = True
        self.target.handle({}, self.req_id)
        self.sender.reply.assert_called_with({}, '-11')
        self.tools.decrease_counter.assert_called()
        assert not self.slow_cache.get.called

    def test_from_slow_cache(self):
        self.parser.get_weather_location.return_value = 'TLL'
        self.fast_cache.__contains__.return_value = False
        self.slow_cache.__contains__.return_value = True
        self.tools.increase_counter.return_value = 1, 1
        self.slow_cache.get.return_value = '-5.5'
        self.target.handle({}, self.req_id)
        self.sender.reply.assert_called_with({}, '-5.5')
        self.tools.decrease_counter.assert_called()
        assert not self.ext_api.get_weather.called
        self.fast_cache.__setitem__.assert_called_with('TLL', '-5.5')

    def test_from_external(self):
        self.parser.get_weather_location.return_value = 'BKK'
        self.fast_cache.__contains__.return_value = False
        self.slow_cache.__contains__.return_value = False
        self.tools.increase_counter.return_value = 1, 1
        self.tools.is_allowed_service.return_value = True
        self.ext_api.get_weather.return_value = '+28.1'
        self.target.handle({}, self.req_id)
        self.sender.reply.assert_called_with({}, '+28.1')
        self.tools.decrease_counter.assert_called()
        self.fast_cache.__setitem__.assert_called_with('BKK', '+28.1')
        self.slow_cache.__setitem__.assert_called_with('BKK', '+28.1')
