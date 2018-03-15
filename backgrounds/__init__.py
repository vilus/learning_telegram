# -*- coding: utf-8 -*-


def _get_celery():
    from .celery import tasks
    return tasks


def _get_thread():
    from .thread import worker
    return worker


def _get_gcp():
    raise NotImplementedError


def get_background(tag='celery'):
    bk_map = {
        'celery': _get_celery,
        'thread': _get_thread,
    }
    return bk_map[tag]()
