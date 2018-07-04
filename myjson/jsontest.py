# coding=utf-8
import unittest
from jsonparser import JsonParser


class TestCase():
    output_file = 'output.txt'
    input_file = 'input.txt'
    test_string1 = '{\"k0\":[{\"k1\":{\"k2\":{\"k3\":[1,2.2,None]}}},' \
                   '[1,\"True\"],[1.999,[\"3.3\",False]]]}'
    test_string2 = '{}'
    test_string3 = '{\"k1\":[[],{}]}'
    test_string4 = '{ \r\n\t   \"k1\"    :    [1,  2  ,  3]}'
    test_string5 = '{\"k1\":True , \"k2\": 123.45, \"k3\": [{},{},{}]}'

    expect_string1 = '{"k0":[{"k1":{"k2":{"k3":[1,2.2,None]}}},' \
                     '[1,"True"],[1.999,["3.3",False]]]}'
    expect_string2 = '{}'
    expect_string3 = '{"k1":[[],{}]}'
    expect_string4 = '{"k1":[1,2,3]}'
    expect_string5 = '{"k3":[{},{},{}],"k2":123.45,"k1":True}'

    load_object = {u'key1': {
        u'key2': {u'key3': [1, 2.2, True, False, None], u'key4': u'val4'}}}

    update_dict = {u'key1': {u'key2': {u'key3': [], u'key4': u'val4'}},
                   u'key5': u'val5', 666: 666}


class TestJsonParser(unittest.TestCase):

    def test_loads_dumps(self):
        # test loads() and dumps()
        jp = JsonParser()
        jp.loads(TestCase.test_string1)
        self.assertEqual(TestCase.expect_string1, jp.dumps())

        jp.loads(TestCase.test_string2)
        self.assertEqual(TestCase.expect_string2, jp.dumps())

        jp.loads(TestCase.test_string3)
        self.assertEqual(TestCase.expect_string3, jp.dumps())

        jp.loads(TestCase.test_string4)
        self.assertEqual(TestCase.expect_string4, jp.dumps())

        jp.loads(TestCase.test_string5)
        self.assertEqual(TestCase.expect_string5, jp.dumps())

    def test_load_file(self):
        # test load_file() , dumps() and dump_dict()
        jp = JsonParser()
        jp.load_file(TestCase.input_file)

        expect_string = '{"key1":{"key2":{"key3":[1,2.2,True,False,None],' \
                        '"key4":"val4"}}}'
        self.assertEqual(expect_string, jp.dumps())

        expect_object = {u'key1': {
            u'key2': {u'key3': [1, 2.2, True, False, None], u'key4': u'val4'}}}
        self.assertEqual(expect_object, jp.dump_dict())

    def test_dump_file(self):
        # test dump_file() and loads()
        jp = JsonParser()
        jp.loads(TestCase.test_string1)
        jp.dump_file(TestCase.output_file)

        jp.loads(TestCase.test_string2)
        jp.dump_file(TestCase.output_file)

        jp.loads(TestCase.test_string3)
        jp.dump_file(TestCase.output_file)

        jp.loads(TestCase.test_string4)
        jp.dump_file(TestCase.output_file)

        jp.loads(TestCase.test_string5)
        jp.dump_file(TestCase.output_file)

    def test_magic_method(self):
        # test __getitem__() , __setitem()__ and loads()
        jp = JsonParser()
        jp.loads(TestCase.test_string5)
        jp['k1'] = 'v1'
        jp['k2'] = 'v2'
        jp['k3'] = 'v3'
        self.assertEqual('v1', jp['k1'])
        self.assertEqual('v2', jp['k2'])
        self.assertEqual('v3', jp['k3'])

    def test_load_dict(self):
        # test load_dict() and dump_dict()
        jp = JsonParser()
        jp.load_dict(TestCase.load_object)
        expect_object = {u'key1': {
            u'key2': {u'key3': [1, 2.2, True, False, None], u'key4': u'val4'}}}
        self.assertEqual(expect_object, jp.dump_dict())

    def test_update(self):
        # test update() and dump_dict()
        jp = JsonParser()
        jp.load_dict(TestCase.load_object)
        jp.update(TestCase.update_dict)
        expect_object = {u'key1': {u'key2': {u'key3': [], u'key4': u'val4'}},
                         u'key5': u'val5'}
        self.assertEqual(expect_object, jp.dump_dict())


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestJsonParser("test_loads_dumps"))
    suite.addTest(TestJsonParser("test_load_dict"))
    suite.addTest(TestJsonParser("test_load_file"))
    suite.addTest(TestJsonParser("test_dump_file"))
    suite.addTest(TestJsonParser("test_magic_method"))
    suite.addTest(TestJsonParser("test_update"))
    unittest.TextTestRunner().run(suite)


if __name__ == '__main__':
    suite()
