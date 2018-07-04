# coding=utf-8
import logging
import copy

logger = logging.getLogger()
logger.setLevel(logging.INFO)

fh = logging.FileHandler('jsonParse.log', mode='a')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


class JsonParser():
    class TokenType:
        start_obj = 1
        end_obj = 2
        start_arr = 4
        end_arr = 8
        null = 16
        comma = 32
        colon = 64
        boolean = 128
        number = 256
        string = 512
        end_file = 1024
        unknown = 2048

    def __init__(self):
        self._data = {}
        self._string = ""
        self.stack_symbol = []
        self.stack_data = []
        self.pos = 0

    def __getitem__(self, key):
        try:
            return self._data[key]
        except KeyError:
            msg = 'dict have no key:' + key
            logger.error(msg, exc_info=True)
            raise KeyError

    def __setitem__(self, key, value):
        try:
            self._data[key] = value
        except (KeyError, AttributeError, TypeError):
            msg = 'dict assignment failed'
            logger.error(msg, exc_info=True)

    def clear(self):
        self._data = {}
        self._string = ""
        self.stack_symbol = []
        self.stack_data = []
        self.pos = 0

    @staticmethod
    def is_space(ch):
        return ch == ' ' or ch == '\t' or ch == '\n' or ch == '\r'

    def read_next_token(self, s):
        status = self.read_next_status(s)
        if status == self.TokenType.start_obj:
            return {'type': self.TokenType.start_obj, 'value': '{'}
        if status == self.TokenType.end_obj:
            return {'type': self.TokenType.end_obj, 'value': '}'}
        if status == self.TokenType.start_arr:
            return {'type': self.TokenType.start_arr, 'value': '['}
        if status == self.TokenType.end_arr:
            return {'type': self.TokenType.end_arr, 'value': ']'}
        if status == self.TokenType.comma:
            return {'type': self.TokenType.comma, 'value': ','}
        if status == self.TokenType.colon:
            return {'type': self.TokenType.colon, 'value': ':'}
        if status == self.TokenType.boolean:
            value = self.read_boolean(s)
            if value:
                return {'type': self.TokenType.boolean, 'value': value}
            else:
                return {'type': self.TokenType.unknown, 'value': None}
        if status == self.TokenType.null:
            value = self.read_null(s)
            if value:
                return {'type': self.TokenType.null, 'value': value}
            else:
                return {'type': self.TokenType.unknown, 'value': None}
        if status == self.TokenType.string:
            value = self.read_string(s)
            if value:
                return {'type': self.TokenType.string, 'value': value}
            else:
                return {'type': self.TokenType.unknown, 'value': None}
        if status == self.TokenType.number:
            value = self.read_number(s)
            if value:
                return {'type': self.TokenType.number, 'value': value}
            else:
                return {'type': self.TokenType.unknown, 'value': None}
        if status == self.TokenType.end_file:
            return {'type': self.TokenType.end_file, 'value': None}
        return {'type': self.TokenType.unknown, 'value': None}

    def read_next_status(self, s):
        while 1:
            if self.pos > len(s) - 1:
                # EOF
                return self.TokenType.end_file
            ch = s[self.pos]
            if not self.is_space(ch):
                break
            self.pos += 1
        if ch == '{':
            self.pos += 1
            return self.TokenType.start_obj
        elif ch == '}':
            self.pos += 1
            return self.TokenType.end_obj
        elif ch == '[':
            self.pos += 1
            return self.TokenType.start_arr
        elif ch == ']':
            self.pos += 1
            return self.TokenType.end_arr
        elif ch == ':':
            self.pos += 1
            return self.TokenType.colon
        elif ch == ',':
            self.pos += 1
            return self.TokenType.comma
        elif ch == '\"':
            self.pos += 1
            return self.TokenType.string
        elif ch == 'N':
            return self.TokenType.null
        elif ch == 'T' or ch == 'F':
            return self.TokenType.boolean
        elif ch == '-':
            return self.TokenType.number
        elif '0' <= ch <= '9':
            return self.TokenType.number
        # throw unkown token
        return self.TokenType.unknown

    def read_string(self, s):
        ret = ""
        while self.pos < len(s) - 1:
            ch = s[self.pos]
            if ch == '\\':
                self.pos += 1
                ech = s[self.pos]
                if ech == '\"':
                    ret += '\"'
                elif ech == '\\':
                    ret += '\\'
                elif ech == '/':
                    ret += '/'
                elif ech == 'b':
                    ret += '\b'
                elif ech == 'f':
                    ret += '\f'
                elif ech == 'n':
                    ret += '\n'
                elif ech == 'r':
                    ret += '\r'
                elif ech == 't':
                    ret += '\t'
                # 还有Unicode转义字符没处理
            elif ch == '\"':
                # end of string
                self.pos += 1
                return unicode(ret)
            else:
                ret += ch
            self.pos += 1
        # 遍历完字符串都没有与前面的"匹配
        msg = 'token can not match: \"'
        logger.error(msg, exc_info=True)
        return None

    def read_boolean(self, s):
        ch_true = s[self.pos: self.pos + 4]
        ch_false = s[self.pos: self.pos + 5]
        if ch_true == 'True':
            self.pos += 4
            return 'True'
        if ch_false == 'False':
            self.pos += 5
            return 'False'
        return None

    def is_number(self, str):
        try:
            float(str)
            return True
        except ValueError:
            msg = 'number invalid:' + str
            logger.error(msg, exc_info=True)
            return False

    @staticmethod
    def is_digital(ch):
        return ch in (
            '.', '+', '-', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'e',
            'E')

    def read_number(self, s):
        num = ""
        while self.pos < len(s) - 1:
            ch = s[self.pos]
            if self.is_digital(ch):
                num += ch
                self.pos += 1
            else:
                break

        if self.is_number(num):
            if '.' in num:
                return float(num)
            else:
                return int(num)
        else:
            return None

    def read_null(self, s):
        ch_null = s[self.pos: self.pos + 4]
        if ch_null == 'None':
            self.pos += 4
            return 'None'
        else:
            return None

    def check_boolen(self, token):
        if token['value'] == 'True' and token['type'] == self.TokenType.boolean:
            token['value'] = True
        elif token['value'] == 'False' and token[
            'type'] == self.TokenType.boolean:
            token['value'] = False
        return token

    def check_null(self, token):
        if token['value'] == 'None' and token['type'] == self.TokenType.null:
            token['value'] = None
        return token

    def match_colon(self, token):
        self.stack_symbol.append(token)
        return True

    def match_comma(self):
        # 遇到逗号时要看stack_symbol栈顶是 [ 还是 {
        top = self.stack_symbol[-1]
        if top['type'] == self.TokenType.start_obj or top[
            'type'] == self.TokenType.colon:
            try:
                value = self.stack_data.pop()
                key = self.stack_data.pop()
                dic = self.stack_data.pop()
                dic[key] = value
                self.stack_data.append(dic)
            except (IndexError, AttributeError, TypeError):
                msg = 'wrong json format, can not solve \",\"'
                logger.error(msg, exc_info=True)
                return False
            else:
                return True
        elif top['type'] == self.TokenType.start_arr:
            try:
                value = self.stack_data.pop()
                lis = self.stack_data.pop()
                lis.append(value)
                self.stack_data.append(lis)
            except (IndexError, AttributeError, TypeError):
                msg = 'wrong json format, can not solve \",\"'
                logger.error(msg, exc_info=True)
                return False
            else:
                return True
        else:
            msg = 'wrong json format, can not solve \",\"'
            logger.error(msg, exc_info=True)
            return False

    def match_end_obj(self):
        # 如果symbol栈栈顶是 '{' 说明data栈栈顶是空字典
        symbol = self.stack_symbol[-1]
        if symbol['type'] == self.TokenType.start_obj:
            try:
                dic = self.stack_data.pop()
                self.stack_data.append(dic)
                # 弹出 '{'
                self.stack_symbol.pop()
            except (IndexError, AttributeError, TypeError):
                msg = 'wrong json format, can not solve \"}\"'
                logger.error(msg, exc_info=True)
                return False
            else:
                return True
        # 如果symbol栈栈顶是 ':' 说明data栈栈顶不是空字典
        elif symbol['type'] == self.TokenType.colon:
            try:
                value = self.stack_data.pop()
                key = self.stack_data.pop()
                dic = self.stack_data.pop()
                dic[key] = value
                self.stack_data.append(dic)
                # 弹出'{'之上的所有':',包括最近的那个'{'
                symbol_top = self.stack_symbol[-1]
                while symbol_top['type'] != self.TokenType.start_obj:
                    self.stack_symbol.pop()
                    symbol_top = self.stack_symbol[-1]
                self.stack_symbol.pop()

            except (IndexError, AttributeError, TypeError):
                msg = 'wrong json format, can not solve \"}\"'
                logger.error(msg, exc_info=True)
                return False
            else:
                return True
        else:
            msg = 'wrong json format, can not solve \"}\"'
            logger.error(msg, exc_info=True)
            return False

    def match_end_arr(self):
        symbol_top = self.stack_symbol[-1]
        if symbol_top['type'] == self.TokenType.start_arr:
            self.stack_symbol.pop()
        else:
            msg = 'wrong json format, can not solve \"]\"'
            logger.error(msg, exc_info=True)
            return False
        data_top = self.stack_data[-1]
        if isinstance(data_top, list) and len(data_top) == 0:
            # 有一个空集
            try:
                lis = self.stack_data.pop()
                lis.append("")
                self.stack_data.append(lis)
            except (IndexError, AttributeError, TypeError):
                msg = 'wrong json format, can not solve \"]\"'
                logger.error(msg, exc_info=True)
                return False
            else:
                return True
        else:
            try:
                value = self.stack_data.pop()
                lis = self.stack_data.pop()
                lis.append(value)
                self.stack_data.append(lis)
            except (IndexError, AttributeError, TypeError):
                msg = 'wrong json format, can not solve \"]\"'
                logger.error(msg, exc_info=True)
                return False
            else:
                return True

    def build(self, token):
        token = self.check_boolen(token)
        token = self.check_null(token)
        if token['type'] == self.TokenType.start_obj:
            self.stack_symbol.append(token)
            self.stack_data.append({})
            return True

        elif token['type'] == self.TokenType.start_arr:
            self.stack_symbol.append(token)
            self.stack_data.append([])
            return True

        elif token['type'] == self.TokenType.colon:
            return self.match_colon(token)

        elif token['type'] == self.TokenType.comma:
            return self.match_comma()

        elif token['type'] == self.TokenType.end_obj:
            return self.match_end_obj()

        elif token['type'] == self.TokenType.end_arr:
            return self.match_end_arr()

        elif token['type'] in [self.TokenType.number, self.TokenType.string,
                               self.TokenType.boolean, self.TokenType.null]:
            self.stack_data.append(token['value'])
            return True
        elif token['type'] == self.TokenType.end_file:
            return True
        else:
            msg = 'wrong json format, invalid token type'
            logger.error(msg, exc_info=True)
            return False

    def check_stack(self):
        if len(self.stack_symbol) > 0:
            top = self.stack_symbol[-1]
            msg = 'wrong json format, can not solve: ' + top['value']
            logger.error(msg, exc_info=True)
            return False
        elif len(self.stack_data) != 1:
            msg = 'wrong json format'
            logger.error(msg, exc_info=True)
            return False
        else:
            self._data = self.stack_data[0]
            return True

    def loads(self, s):
        self.clear()
        token = self.read_next_token(s)
        while token:
            if self.build(token):
                if token['type'] == self.TokenType.end_file:
                    break
                else:
                    token = self.read_next_token(s)
            else:
                self.pos = 0
                self._data = {}
                return
        self.check_stack()

    def dumps_helper(self, obj):
        if isinstance(obj, dict):
            self._string += '{'
            for idx, (key, value) in enumerate(obj.items()):
                self._string += '\"'
                self._string += key
                self._string += '\"'
                self._string += ':'
                self.dumps_helper(value)
                if idx < len(obj) - 1:
                    self._string += ','
            self._string += '}'
        elif isinstance(obj, list):
            self._string += '['
            for x in range(len(obj)):
                self.dumps_helper(obj[x])
                if x != len(obj) - 1:
                    self._string += ','
            self._string += ']'
        elif isinstance(obj, unicode):
            self._string += '\"'
            self._string += obj
            self._string += '\"'
        else:
            self._string += str(obj)

    def dumps(self):
        self._string = ""
        self.dumps_helper(self._data)
        return self._string

    def dump_dict(self):
        ret_data = copy.deepcopy(self._data)
        return ret_data

    def load_file(self, f):
        try:
            with open(f) as file_object:
                contents = file_object.read()
        except IOError:
            msg = 'file can not found, or read file failed'
            logger.error(msg, exc_info=True)
        else:
            self.loads(contents)

    def dump_file(self, f):
        dump_string = self.dumps()
        try:
            with open(f, 'a') as file_object:
                file_object.write(dump_string)
                file_object.write('\n')
        except IOError:
            msg = 'file can not found, or write file failed'
            logger.error(msg, exc_info=True)

    def load_dict_helper(self, obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                self.load_dict_helper(value)
            self._string += '}'
        elif isinstance(obj, list):
            self._string += '['
            for x in range(len(obj)):
                self.dumps_helper(obj[x])
                if x != len(obj) - 1:
                    self._string += ','
            self._string += ']'
        elif isinstance(obj, unicode):
            self._string += '\"'
            self._string += obj
            self._string += '\"'
        else:
            self._string += str(obj)

    def load_dict_helper(self, dic):
        if isinstance(dic, dict):
            ret_dic = {}
            for key, value in dic.items():
                if not isinstance(key, (str, unicode)):
                    continue
                else:
                    ret_value = self.load_dict_helper(value)
                    ret_dic[key] = ret_value
            return ret_dic
        elif isinstance(dic, list):
            ret_list = []
            for value in dic:
                ret_value = self.load_dict_helper(value)
                ret_list.append(ret_value)
            return ret_list
        else:
            return dic

    def load_dict(self, d):
        self.clear()
        dic = copy.deepcopy(d)
        self._data = self.load_dict_helper(dic)

    def update(self, d):
        dic = copy.deepcopy(d)
        if isinstance(dic, dict):
            for key, value in dic.items():
                if not isinstance(key, (str, unicode)):
                    continue
                else:
                    self._data[key] = value
        else:
            self._data = dic
