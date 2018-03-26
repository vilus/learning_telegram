# -*- coding: utf-8 -*-


def _get_celery():
    from .celery import tasks
    return tasks


def _get_thread():
    from .thread import worker
    return worker


def _get_gcp():
    raise NotImplementedError


def get_background(conf):
    # background must have method `run(cmd, conf, params)`
    tag = conf.get('bg_type', 'celery')
    bg_map = {
        'celery': _get_celery,
        'thread': _get_thread,
    }
    return bg_map[tag]()
