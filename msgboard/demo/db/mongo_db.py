import math
from demo.db import rankBoard, usrInfo, msgBoard


class RankBoardMongo():

    @staticmethod
    def drop():
        rankBoard.drop()

    @staticmethod
    def is_rank_empty():
        return rankBoard.count() is 0

    @staticmethod
    def get_top_rank(top):
        rank_board = rankBoard.find({}, {'_id': 0}).sort('msg_num', -1).limit(
            top)
        ret = []
        for item in rank_board:
            ret.append(item)
        return ret

    @staticmethod
    def update_rank(nickname):
        res = rankBoard.find_and_modify({"nick_name": nickname},
                                        {"$inc": {"msg_num": 1}}, new=True)
        if res is None:
            rankBoard.insert({"nick_name": nickname, "msg_num": 1})
            return 1
        else:
            return res['msg_num']


class MsgBoardMongo():

    @staticmethod
    def drop():
        msgBoard.drop()

    @staticmethod
    def is_msg_empty():
        return msgBoard.count() is 0

    @staticmethod
    def total_page(pre_page):
        total_page = int(math.ceil(msgBoard.count() * 1.0 / pre_page))
        return total_page

    @staticmethod
    def get_msg(skip_idex, limit_idex):
        msg_board = msgBoard.find({}, {'_id': 0})
        sort_msg_board = msg_board.sort([('time_float', -1)]).skip(
            skip_idex).limit(limit_idex)
        ret = []
        for item in sort_msg_board:
            ret.append(item)
        return ret

    @staticmethod
    def get_all_msg():
        msg_board = msgBoard.find({}, {'_id': 0})
        ret = []
        for item in msg_board:
            ret.append(item)
        return ret

    @staticmethod
    def get_all_rank():
        rank_board = rankBoard.find({}, {'_id': 0})
        ret = []
        for item in rank_board:
            ret.append(item)
        return ret

    @staticmethod
    def submit_msg(nickname, message, time_stamp, time_float):
        msgBoard.insert(
            {"nick_name": nickname, "message": message, "time": time_stamp,
             'time_float': time_float})


class Account():

    @staticmethod
    def find_usr_by_phone(telephone):
        return usrInfo.find_one({'telphone': str(telephone)})

    @staticmethod
    def register(usr):
        usrInfo.insert(usr)
