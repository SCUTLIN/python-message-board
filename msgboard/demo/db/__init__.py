#!/usr/bin/env python
# coding=utf-8
import pymongo
import json
from demo.log.Logger import logger
conf = {}
try:
    with open('./db/mongo.conf') as file_object:
        contents = file_object.read()
        conf = json.loads(contents)
except IOError:
    msg = 'read redis configure failed'
    logger.exception(msg)

host = conf['host']
port = conf['port']

mongoConn = pymongo.MongoClient(host, port)
database = mongoConn.netease
dataTable = database.vote_info

rankBoard = database.rank_board
usrInfo = database.usr_info
msgBoard = database.msg_board

msgBoard.create_index([("time_float", -1)])
rankBoard.create_index([("msg_num", -1)])
