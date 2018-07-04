from jsonparser import JsonParser
import json
jp = JsonParser()
s6 = '{\"k1\":1223 , \"k2\": 123.45, \"k3\": {\"k4\":1}}'
str2 = '{\"k0\":{\"k1\":{}}}'
str1 = '{\"k0\":[{\"k1\":{\"k2\":{\"k3\":[1,2.2,None]}}},[1,\"True\"],[1.999,[\"3.3\",False]]]}'

jp.loads(s6)
jp['k1'] = 1
jp['k2'] = 2
jp['k3']['k4'] = 666
print jp.dump_dict()
print jp['k1']
