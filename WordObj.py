import json
import re
import random
from rich.table import Table
from rich.console import Console
class WordObj():
    """
    如果是对单个单词使用，可以不配置路径，只要涉及到多个单词都需在实例Wo时配置文件路径，
    """
    def __init__(self,
                 wid=None,
                 group=[],
                 word=None,
                 chines=None,
                 accuracy=[1,1,0.99],
                 tips=None,
                 example=None,
                 first_time=None,
                 last_time=None,
                 path=None):
        self.wid=wid
        self.group=group
        self.word=word
        self.chines=chines
        self.accuracy=accuracy
        self.tips=tips
        self.example=example
        self.first_time=first_time
        self.last_time=last_time
        self.path=path
    #对单个单词操作
    def get_tips(self):
        return self.tips
    def get_example(self):
        return self.example
    def get_word_dict(self):#返回单词元素的所有信息
        word_param={
            "wid":self.wid,
            "group":self.group,
            "word":self.word,
            "chines":self.chines,
            "accuracy":self.accuracy,
            "tips":self.tips,
            "example":self.example,
            "first_time":self.first_time,
            "last_time":self.last_time
        }
        return word_param
    def set_wid(self,last_id):
        self.wid=last_id+1
    def set_group(self,group_name):
        self.group=group_name
    def set_word(self,strs):
        """
        根据输入的英文和中文字符串，分别匹配出单词和中文赋予self.word和self.chines的值
        :param strs: 包含英文和中文的字符串输入(眼睛eye)
        :return:
        """
        try:
            zhong_compile = re.compile("[\u4e00-\u9fa5;；]+")
            ying_compile = re.compile("[a-zA-Z]+")
            cixing_compile = re.compile("[<《]([^>》]+)")#[>》]
            zhongwen = re.search(zhong_compile, strs)
            yingwen = re.search(ying_compile, strs)
            cixing = re.search(cixing_compile, strs)
            if zhongwen==None or yingwen==None:
                return "格式错误"
            else:
                if cixing!=None:
                    cixing = cixing.group(1)
                    self.chines = "(" + cixing + ")" + zhongwen.group()
                    self.word=yingwen.group()
                    return (self.word,self.chines,cixing)
                else:
                    self.chines = zhongwen.group()
                    self.word = yingwen.group()
                    return (self.word, self.chines)




        except:
            print("请按格式输入")


    #对单词字典进行操作方法，不对单个单词属性进行修改
    def set_path(self,path):
        self.path=path
        return self.path
    def set_accuracy(self,words, x, is_add="add"):
        """
        这个方法是对于一个大的字典进行操作，不对实例对象进行修改
        :param words:多个单词组成的字典 x:要修改单词的字符串 is_add:增加"add"还是减少"less"正确率
        :return:
        """
        if is_add == "add":
            if words.get(x, 0) != 0:
                this = words[x]["accuracy"]
                this[0] += 1
                this[1] += 1
                this[2] = round(this[1] / this[0], 2)
                print(f"{x}，accuracy:{this[2]}")
            else:
                print("未找到")
        else:
            if words.get(x, 0) != 0:
                this = words[x]["accuracy"]
                this[0] += 1
                this[2] = round(this[1] / this[0], 2)
                print(f"{x}，accuracy:{this[2]}")
            else:
                print("未找到")
    def create_eve(self,words):
        """
        根据words中accuracy正确率生成对应words字典的频数分布列表
        :param words:多个单词组成的字典
        :return: list=['eye', 'system', 'system', 'yes', 'yes', 'yes', 'yes', 'yes']]
        """
        random_words_keys=[]
        lists=[]
        eve = {}
        sum = 0
        words_key=list(words.keys())
        for i in range(20):
            random_words_keys.append(random.choice(words_key))
        for i in random_words_keys:
            sum += 1 - words[i]["accuracy"][2]

        for i in random_words_keys:
            eve[i] = round((1 - words[i]["accuracy"][2]) / sum, 2)
        print(f"单词出现占比{eve}")
        for i in eve:
            num = (eve[i] * 100) // 10
            if num < 1:
                num = 1
            else:
                num = int(num)
            for x in range(num):
                lists.append(i)
        return lists
    def load_words(self,path=None):
        if path==None:
            path=self.path
        else:
            path=path
        words=None
        with open(path,"r",encoding="utf-8") as f:
            words=json.load(f)
        return words
    def save_words(self,words,path):
        """
        保存文件
        :param words:
        :param path:
        :return:
        """
        if path==None:
            path=self.path
        else:
            path=path
        with open(path,"w",encoding="utf-8") as f:
            f.seek(0, 2)  # seek方法是第一个参数是偏移量，第二个参数是位置0是开头，1是当前位置，2是末尾
            shuchu = json.dumps(words, ensure_ascii=False, indent=4)
            f.write(shuchu)
    def updata_word(self,word_param,words=None,path=None):
        """
        将单独一个单词属性字典写回json中,一般不单独使用，常联合调用
        :param word_param:
        :param words:
        :param path:
        :return:
        """
        if path==None:
            path=self.path
        else:
            path=path

        if words==None:
            words=self.load_words(path)
        else:
            words=words
        if word_param=="没找到":
            print("修改单词属性失败")
        else:
            words[word_param["word"]]=word_param
            self.save_words(words,path)
    def set_tips(self):
        # 调用大模型api
        pass
    def set_example(self):
        # 调用大模型api
        pass
    def search_word_param_copy(self,word,path=None):
        """
        从文件里查找单词,返回的是单词的属性，只是单词属性的拷贝，本方法不对对单词数据进行改变
        :param word:
        :param path:
        :return: ["dict",""没找到""]返回的是单词属性的字典
        """
        wordobj=None
        if path==None:
            path=self.path
        else:
            path=path
        with open(path,"r",encoding="utf-8") as f:
            word_list=json.load(f)
            tag=False
            for i in word_list:
                if word_list[i]["word"]==word:
                    wordobj=word_list[word]
                    tag=True
                    return wordobj
                else:
                    pass
            if tag==False:
                return "没找到"
    def show_words(self,words=None):
        if words==None:
            words=self.load_words(self.path)
        control=Console()

        table=Table(title="Words Table")
        table.add_column("word",style="green")
        table.add_column("chines")
        table.add_column("count")
        table.add_column("right")
        table.add_column("accuracy")
        table.add_column("first_time")
        table.add_column("last_time")

        for i in words:
            table.add_row(i,
                          str(words[i]["chines"]),
                          str(words[i]["accuracy"][0]),
                          str(words[i]["accuracy"][1]),
                          str(words[i]["accuracy"][2]),
                          str(words[i]["first_time"]),
                          str(words[i]["last_time"]))
        control.print(table)












