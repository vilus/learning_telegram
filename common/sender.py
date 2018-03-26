# -*- coding: utf-8 -*-
import logging
from requests import post


class TlmSender:
    """
    Hard dependency from weather_handler (inner assumption)
    """
    def __init__(self, back_api):
        self.back_api = back_api

    def reply(self, back_data, value):
        back_data['message']['text'] = back_data['message']['text'].format(value)
        logging.debug('try send reply\n {0}\n to {1}\n'.format(back_data, self.back_api))
        post(self.back_api, json=back_data)


def get_sender(conf):
    return TlmSender(conf['back_api'])
