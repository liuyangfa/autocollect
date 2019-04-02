# -*- coding: utf-8 -*-
from django.apps import AppConfig
import os

default_app_config = 'demo.DemoConfig'


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class DemoConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = u"基础数据"
