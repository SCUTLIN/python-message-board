#!/usr/bin/env python
# coding=utf-8
import hashlib
import uuid
import math
import json
from demo.cache import redisHandler, redisPipe


class SessionCache:
    CookieID = 'flask_session_cache'
    ExpireSeconds = 10 * 60

    def __init__(self, handler):
        self.handler = handler
        session_id = self.handler.get(SessionCache.CookieID, None)
        if session_id and redisHandler.exists(session_id):
            self.session_id = session_id
        else:
            self.session_id = self.session_key()
            self.handler[SessionCache.CookieID] = self.session_id
            redisHandler.hset(self.session_id, None, None)
        redisHandler.expire(self.session_id, SessionCache.ExpireSeconds)

    def session_key(self):
        UUID = str(uuid.uuid1()).replace('-', '')
        MD5 = hashlib.md5()
        MD5.update(bytes(UUID))
        session_key = MD5.hexdigest()
        return session_key

    def __setitem__(self, key, value):
        redisHandler.hset(self.session_id, key, value)

    def __getitem__(self, key):
        return redisHandler.hget(self.session_id, key)

    def __delitem__(self, key):
        redisHandler.hdel(self.session_id, key)

    def add_map(self, map_data):
        for item in map_data.items():
            redisPipe.hset(self.session_id, item[0], item[1])
        redisPipe.execute()

    def get_all(self):
        return redisHandler.hgetall(self.session_id)


class RankBoardCache:
    ExpireSeconds = 100 * 60

    @staticmethod
    def drop():
        redisHandler.delete('rank_board_cache')

    @staticmethod
    def is_rank_cache_empty():
        return redisHandler.zcard('rank_board_cache') is 0

    @staticmethod
    def update_rank_cache(nickname, msgnum):
        redisHandler.zadd('rank_board_cache', nickname, msgnum)
        redisHandler.expire('rank_board_cache', RankBoardCache.ExpireSeconds)

    @staticmethod
    def get_top_rank_cache(top):
        rank_cache = redisHandler.zrevrange('rank_board_cache',
                                            start=0,
                                            end=top,
                                            withscores=True)
        ret = []
        for item in rank_cache:
            append_item = {'nick_name': item[0], 'msg_num': item[1]}
            ret.append(append_item)
        return ret

    @staticmethod
    def load_from_mongo(rank_board):
        for item in rank_board:
            msgnum = item['msg_num']
            nickname = item['nick_name']
            redisHandler.zadd('rank_board_cache', nickname, msgnum)
            redisHandler.expire('rank_board_cache',
                                RankBoardCache.ExpireSeconds)

class MsgBoardCache:
    ExpireSeconds = 100 * 60

    @staticmethod
    def drop():
        redisHandler.delete('msg_board_cache')

    @staticmethod
    def load_from_mongo(msg_board):
        for item in msg_board:
            time_float = item['time_float']
            msg = json.dumps(item)
            redisHandler.zadd('msg_board_cache', msg, time_float)
            redisHandler.expire('msg_board_cache', MsgBoardCache.ExpireSeconds)

    @staticmethod
    def is_msg_cache_empty():
        return redisHandler.zcard('msg_board_cache') is 0

    @staticmethod
    def total_page(pre_page):
        total_page = int(
            math.ceil(redisHandler.zcard('msg_board_cache') * 1.0 / pre_page))
        return total_page

    @staticmethod
    def get_msg_cache(start, end):
        msg_cache = redisHandler.zrevrange('msg_board_cache',
                                           start=start,
                                           end=end,
                                           withscores=False)
        ret = []
        for item in msg_cache:
            ret.append(json.loads(item))
        return ret

    @staticmethod
    def submit_msg_cache(msg, time_float):
        msg = json.dumps(msg)
        redisHandler.zadd('msg_board_cache', msg, time_float)
        redisHandler.expire('msg_board_cache', MsgBoardCache.ExpireSeconds)
