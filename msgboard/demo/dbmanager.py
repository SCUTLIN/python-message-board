#!/usr/bin/env python
# coding=utf-8
from demo.cache.redis_cache import RankBoardCache, MsgBoardCache
from demo.db.mongo_db import RankBoardMongo, MsgBoardMongo, Account


class DbManager():

    @staticmethod
    def db_msg_total_page(pre_page):
        return MsgBoardMongo.total_page(pre_page)

    @staticmethod
    def cache_msg_total_page(pre_page):
        return MsgBoardCache.total_page(pre_page)

    @staticmethod
    def cache_load_msg_from_db():
        all_msg = MsgBoardMongo.get_all_msg()
        MsgBoardCache.load_from_mongo(all_msg)

    @staticmethod
    def cache_load_rank_from_db():
        all_rank = MsgBoardMongo.get_all_rank()
        RankBoardCache.load_from_mongo(all_rank)

    @staticmethod
    def get_msg(curr_page, pre_page):
        if MsgBoardCache.is_msg_cache_empty():
            ret_msg = MsgBoardMongo.get_msg((curr_page - 1) * pre_page,
                                            pre_page)
            DbManager.cache_load_msg_from_db()
            return ret_msg
        else:
            ret_msg = MsgBoardCache.get_msg_cache((curr_page - 1) * pre_page,
                                                  curr_page * pre_page - 1)
            return ret_msg

    @staticmethod
    def submit_msg(nickname, message, time_stamp, time_float):
        MsgBoardMongo.submit_msg(nickname, message, time_stamp, time_float)
        res = RankBoardMongo.update_rank(nickname)
        if RankBoardCache.is_rank_cache_empty():
            DbManager.cache_load_rank_from_db()
        MsgBoardCache.submit_msg_cache(
            {"nick_name": nickname, "message": message, "time": time_stamp},
            time_float)
        RankBoardCache.update_rank_cache(nickname, res)

    @staticmethod
    def get_rank(top):
        if RankBoardCache.is_rank_cache_empty():
            ret_rank = RankBoardMongo.get_top_rank(top)
            RankBoardCache.load_from_mongo(ret_rank)
            return ret_rank
        else:
            ret_rank = RankBoardCache.get_top_rank_cache(top)
            return ret_rank

    @staticmethod
    def find_usr_by_phone(telephone):
        return Account.find_usr_by_phone(telephone)

    @staticmethod
    def register(usr):
        Account.register(usr)


