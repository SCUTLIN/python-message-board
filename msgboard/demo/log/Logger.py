#!/usr/bin/env python
# coding=utf-8
import logging
from logging.handlers import RotatingFileHandler
from demo.log.Config import config

defaultDebugMode = True
defaultLogLevel = logging.DEBUG
defaultLogFile = 'default.log'
defaultLogFmt = '%(message)s'

debug = defaultDebugMode
level = defaultLogLevel
logfile = defaultLogFile
fmt = defaultLogFmt

logConfig = config.get('logger')
if logConfig:
    debug = defaultDebugMode if logConfig.get('debugMode') is None else logConfig.get('debugMode')
    level = logConfig.get('level') or defaultLogLevel
    logfile = logConfig.get('logFile') or defaultLogFile
    fmt = logConfig.get('fmt') or defaultLogFmt

logger = logging.getLogger(__name__)
logger.setLevel(level=level)
__formatter = logging.Formatter(fmt)

if debug:
    __console = logging.StreamHandler()
    __console.setLevel(level)
    __console.setFormatter(__formatter)
    logger.addHandler(__console)
else:
    __rHandler = RotatingFileHandler(logfile, maxBytes=1 * 1024 * 1024, backupCount=3)
    __rHandler.setLevel(level)
    __rHandler.setFormatter(__formatter)
    logger.addHandler(__rHandler)

