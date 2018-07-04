#!/usr/bin/env python
# coding=utf-8
import logging

config = {
    'logger': {
        'level': logging.DEBUG,
        'debugMode': False,
        'logFile': 'default.log',
        'fmt': '%(asctime)s|%(levelname)s|%(filename)s(%(funcName)s:%(lineno)d)|%(message)s',
    },

}
