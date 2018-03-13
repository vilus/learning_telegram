# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import Celery

# TODO: from ENV
# broker_url = 'redis://:password@host:port/db_number'

app = Celery(
    'background',
    broker='redis://',
    backend='redis://',
    include=['background.tasks']
)

'''
task_routes = {
    'get_weather': 'external_api',
    'send_to': 'internal_api',
}
'''

app.conf.update(
    task_send_sent_event=True,
    worker_hijack_root_logger=False
)

if __name__ == '__main__':
    app.start()

