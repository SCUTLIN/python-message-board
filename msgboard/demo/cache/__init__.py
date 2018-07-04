#!/usr/bin/env python
# coding=utf-8
import redis
import json
from demo.log.Logger import logger
conf = {}
try:
    with open('./cache/redis.conf') as file_object:
        contents = file_object.read()
        conf = json.loads(contents)
except IOError:
    msg = 'read redis configure failed'
    logger.exception(msg)

host = conf['host']
port = conf['port']

redisPool = redis.ConnectionPool(host=host, port=port, decode_responses=True)
redisHandler = redis.Redis(connection_pool=redisPool)
redisPipe = redisHandler.pipeline(transaction=True)
