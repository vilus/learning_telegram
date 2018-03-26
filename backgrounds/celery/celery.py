# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
import sys
from celery import Celery


broker_url = os.environ['TLM_BROKER_URL']


app = Celery(
    'background',
    broker=broker_url,
    backend=broker_url,
    include=['backgrounds.celery.tasks']
)


app.conf.update(
    task_send_sent_event=True,
    worker_hijack_root_logger=False
)

sys.path.append('.')
sys.path.append('..')  # ^(
sys.path.append('...')

if __name__ == '__main__':
    app.start()
