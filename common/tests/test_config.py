# -*- coding: utf-8 -*-
import mock
import os
from ..config import get_conf, PREFIX


first_param = 'FIRST_PARAM'
first_value = 'first_value'
second_param = 'SECOND_PARAM'
second_value = 'second_value'


def test_conf_from_ini():
    pass


def test_conf_from_db():
    pass


@mock.patch.dict(os.environ, {PREFIX+first_param: first_value, PREFIX+second_param: second_value})
def test_conf_from_env():
    conf = get_conf(src='env')
    assert conf[first_param] == first_value
    assert conf[second_param] == second_value
