培训作业：json解析器
    （1）基于Python 2.7封装实现一个可重用的Json解析类，具体要求为:
    1、该类能读取JSON格式的数据，并以Python字典的方式读写数据；
    2、给定一个Python字典，可以更新类中数据，并以JSON格式输出；
    3、遵循JSON格式定义确保相同的同构数据源彼此转换后数据仍然一致；
    4、支持将数据以JSON格式存储到文件并加载回来使用；
    5、只允许使用Python string、unittest和logging模块，不允许使用eval、其他标准模块及任何第三方开发库；
    6、独立完成此作业，不要参考任何现成代码。模块需要附带测试代码及一份简短的模块使用说明；使用git记录代码提交历史，使用unittest编写测试用例。

    （2）文件结构
    jasonparse.py:
    loads(self, s) 读取JSON格式数据，输入s为一个JSON字符串，无返回值；
    dumps(self) 将实例中的内容转成JSON格式返回；
    load_file(self, f) 从文件中读取JSON格式数据, 无返回值；
    dump_file(self, f) 将实例中的内容以JSON格式存入文件；
    load_dict(self, d) 从dict中读取数据，存入实例中；
    dump_dict(self) 返回一个字典，包含实例中的内容；
    __getitem__() , __setitem__ ,JsonParser类支持用[]进行赋值、读写数据的操作，类似字典
    update(self, d)用字典d更新实例中的数据

    jasontest.py:单元测试

    input.txt:测试输入的文件

    output.txt:测试输出的文件

    jsonParse.log:日志

    （3）目前的问题：
    1.还未解析Unicode转义字符
    2.遇到类似[1,2,3,]在末尾多一个逗号的情况会解析失败
    3.为了避免返回成员的引用和使用入参的引用，使用了copy模块的deepcopy，不符合约束
    4.
