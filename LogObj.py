import json
import os.path
import time
from config_user import config
import util
from util import show_choies_file
from WordObj import WordObj as WO
from config_user import config
from rich.table import Table
from rich.console import Console
from AiObj import AiObj
class LogObj():
    """
    在所有模式的最开始进行实例化

    只要实例化后对象内，就能从logobj中直接调用出words单词字典和word_table单词日志
    """
    def __init__(self,
                 word_path=None,
                 words=None):
        """
        只要指定了word_path，单词字典就确定了
        :param word_path: 指定单词文件路径
        """
        self.word_table={}
        self.word_path=word_path#word文件的路径
        self.log_path=None
        self.max_wrong_word=None
        self.Wo=WO(path=word_path)
        self.words=self.local_log_words(words)
    def log_add_word(self,word):
        if word=="今日完成":#今日完成是日志的最后一个标志
            self.word_table[word] = {
                "max_wrong_word":self.max_wrong_word,
                "log_path":self.log_path,
                "end_time":time.strftime("%Y-%m-%d_%H:%M:%S")
            }
        else:
            word_param = self.words[word]
            if self.word_table.get(word,False):
                pass
            else:
                word_each_log = {
                    "this_all": 0,
                    "this_right": 0,
                    "word_param": word_param,
                    "this_accuracy": 0,
                    "think_time": [],
                    "last_time": time.strftime("%Y-%m-%d_%H:%M:%S")
                }
                self.word_table[word]=word_each_log
    def load_log(self):
        """

        :return: 返回的是字典，一个是日志内容，一个是返回选择加载的日志路径，用于save_log对某一次日志的修改
        """
        log_path=show_choies_file(config["root_log_lib_path"])
        self.log_path=log_path
        with open(self.log_path,"r",encoding="utf-8") as f:
            word_table=json.load(f)
        return {"word_table" :word_table,"log_path":log_path}
    def save_log(self,log_path=None):
        """
        保存日志文件，一般不用配置log_path，文件名会已时间进行命名
        :param log_path: 日志文件的路径
        :return:
        """
        if log_path==None:
            log_path=os.path.join(f"./log_lib",f"{time.strftime('%Y-%m-%d_%H_%M')}.json")
        with open(log_path,"w",encoding="utf-8") as f:
            f.seek(0, 2)  # seek方法是第一个参数是偏移量，第二个参数是位置0是开头，1是当前位置，2是末尾
            shuchu = json.dumps(self.word_table, ensure_ascii=False, indent=4)
            f.write(shuchu)
        print("save_log_this")
    def local_log_words(self,words):
        """
        在实例化时调用，不单独使用
        在logobj中构建一个words，用于直接调用单词字典，并直接写入logobj的属性中，实例化一个logobj就直接构建好单词字典
        :param words:
        :return:
        """
        if words==None:
            words=self.Wo.load_words(self.word_path)
        else:
            words=words
        return words
    def is_in_table(self,word):
        if word in self.word_table.keys():
            return True
        else:
            return False
    def set_word_log(self,word,result):
        """
        这里整合了单词和日志的同时修改
        修改logtable的同时要修改单词属性并保存单词文件
        :param word:
        :param result: ["right","wrong"]
        :return:
        """
        if self.is_in_table(word):
            log_param=self.word_table[word]
            log_param["this_all"]+=1
            log_param["word_param"]["accuracy"][0] +=1
            if result=="right":#如果是正确的，执行以下代码
                #修改该单词的日志信息
                log_param["this_right"]+=1
                log_param["this_accuracy"]=round(log_param["this_right"]/log_param["this_all"]-0.01,2)
                log_param["last_time"]=time.strftime('%Y-%m-%d_%H:%M:%S')
                log_param["word_param"]["accuracy"][1] += 1
                log_param["word_param"]["accuracy"][2] = round(log_param["word_param"]["accuracy"][1]/log_param["word_param"]["accuracy"][0]-0.01,2)
                log_param["word_param"]["last_time"]=time.strftime('%Y-%m-%d_%H:%M:%S')
            elif result == "wrong":
                log_param["this_accuracy"] = round(log_param["this_right"] / log_param["this_all"] - 0.01,2)
                log_param["last_time"] = time.strftime('%Y-%m-%d_%H:%M:%S')
                log_param["word_param"]["accuracy"][2] = round(log_param["word_param"]["accuracy"][1] / \
                                                         log_param["word_param"]["accuracy"][0] - 0.01,2)
                log_param["word_param"]["last_time"] = time.strftime('%Y-%m-%d_%H:%M:%S')
        else:
            print("修改失败")
    def from_logobj_updata_words_file(self):
        """
        把运行中单词字典保存回单词文件中
        :return:
        """
        self.Wo.save_words(self.words,self.word_path)
    def show_log(self,batch_log):
        console = Console()

        # 创建表格
        table = Table(title="Log Table")

        # 添加列
        table.add_column("word", justify="left", style="green")
        table.add_column("this_all", justify="left", style="green")
        table.add_column("this_right", justify="left", style="green")
        table.add_column("this_accuracy", justify="left", style="green")
        table.add_column("history_accuracy", justify="left", style="green")
        table.add_column("time", justify="left", style="green")

        # 添加行
        for i in batch_log:
            if i=="今日完成":
                table2=Table()
            else:
                table.add_row(i,
                          str(batch_log[i]["this_all"]),
                          str(batch_log[i]["this_right"]),
                          str(batch_log[i]["this_accuracy"]),
                          str(batch_log[i]["word_param"]["accuracy"][2]),
                          str(batch_log[i]["last_time"]))

        # 显示表格
        console.print(table)

    def from_group_to_everyday(self, everyday, tag):
        batch_everyday = {}
        finded=False
        for i in everyday:
            group_list = everyday[i]["group"]
            for x in group_list:
                if x == tag:
                    finded=True
                    batch_everyday[i] = everyday[i]
                else:
                    pass
        if finded==False:
            print("未找到拥有该标签的词汇，已切换成全部词汇")
            time.sleep(1.5)
            return everyday
        else:
            return batch_everyday
    def batch_word_add_group(self,group_name,words_name_list):
        if len(words_name_list)!=0:
            for i in words_name_list:
                word_param=self.words.get(i,False)
                if word_param:
                    word_param["group"].append(group_name)
                    print(f"{i}:添加成功")
                else:
                    print(f"{i}:添加失败")
            self.Wo.save_words(self.words,self.word_path)
        else:
            print("syntax error:新增单词列表有误")

    def commond_control(self,commond, words_path):
        """
        commond_list={
            "word":{

                "group":{
                    "create":"(输入组名)创建一个新组",
                    "remove":"(输入组名)删除一个组，并移出组内单词",
                    "(输入组名)":{
                        "add":"(输入单词1 单词2 单词3)可多选，往组内添加指定单词",
                        "remove":"(输入单词1 单词2 单词3可多选，往组内移除指定单词)"
                    }
                },
                "name":{
                    (输入单词名)word1:{#以下为关键词
                    "en":"单词本身不能重置",
                    "chines":"(输入新的翻译)重置中文",
                    "wid":"(输入id号)重置id",
                    "tips":"(无参数)重新获取提示",
                    "example":"(无参数)重新获取",
                    "add_group":"(输入组名可多选)把单词添加到指定组内",
                    "remove_group":（输入组名可多选）把单词从指定组移除"
                    }
                }


            },
            "kong_lib":{},
            "log_lib":{},
            "system":{}
        }
        :return:
        """
        config_system=util.load_json(config["config_system"])
        commond_list = commond.split(" ")
        commond_len=len(commond_list)
        layer = 0
        if util.re_complish(commond_list[layer],"word") and commond_len>layer+1:
            layer = 1
            if util.re_complish(commond_list[layer],"group") and commond_len>layer+1:
                layer = 2
                #word group create []
                if util.re_complish(commond_list[layer],"create") and commond_len>layer+1:
                    # 创建
                    layer = 3
                    for i in commond_list[layer:]:
                        if i not in config_system["all_groups"]:
                            config_system["all_groups"].append(i)
                            print(f"<{i}>组创建成功")
                        else:
                            print(f"<{i}>组已存在")
                elif util.re_complish(commond_list[layer],"remove") and commond_len>layer+1:
                    layer = 3
                    for x in self.words:#删除所有单词中的该标签
                        if commond_list[layer] in self.words[x]["group"]:
                            self.words[x]["group"].remove(commond_list[layer])
                    for i in commond_list[layer:]:
                        if i in config_system["all_groups"]:
                            config_system["all_groups"].remove(i)
                        else:
                            print(f"未存在<{i}>")
                elif util.re_complish(commond_list[layer],"show") and commond_len==layer+1:
                    print(config_system["all_groups"])
                elif util.re_complish(commond_list[layer],"name")and commond_len>layer+2:  # 为组批量添加单词
                    #word group name [] [word1] [word2]
                    layer = 3
                    if commond_list[layer] in config_system["all_groups"]:
                        group_name = commond_list[layer]
                        word_list = commond_list[layer + 1:]
                        self.batch_word_add_group(group_name,word_list)
                    else:
                        print(f"未创建组<{commond_list[layer]}>")
                else:
                    print("syntax error")
            elif util.re_complish(commond_list[layer],"delete")and commond_len>layer+1:
                #word delete [] []
                layer =2
                for i in commond_list[layer:]:
                    delete_result=self.words.pop(i,False)
                    if delete_result:
                        print(f"delete '{delete_result['word']}' succeed")
                    else:
                        print(f"no '{delete_result['word']}'")
            elif util.re_complish(commond_list[layer], "add")and commond_len>layer+1:
                layer = 2
                for i in commond_list[layer:]:
                    wo = WO()
                    set_word_tag = wo.set_word(i)  # 根据输入的word字符串，如：“sys眼睛”，分给给单词实例对象的word，chines属性进行赋值
                    if set_word_tag != "格式错误":
                        self.words[f"{wo.word}"] = wo.get_word_dict()
                        self.words[f"{wo.word}"]["group"] = [time.strftime("%Y-%m-%d")]  # 换成时间切换函数
                        cixing = util.set_group_cixing(i)
                        if cixing:
                            self.words[f"{wo.word}"]["group"].extend(cixing)
                        self.words[f"{wo.word}"]["first_time"] = time.strftime("%Y-%m-%d_%H:%M:%S")  # 设置首次创建时间
                        self.words[f"{wo.word}"]["last_time"] = time.strftime("%Y-%m-%d_%H:%M:%S")  # 设置最新出现时间
                        print(f"write '{wo.word}' succeed!")
                    else:
                        print(f"write '{wo.word}' faild! syntax error：未给出英文或翻译")
            elif util.re_complish(commond_list[layer], "name")and commond_len>layer+1:
                #word name word1 [wid] [参数]
                layer=2
                if len(commond_list)>layer:
                    word_name = commond_list[layer]
                    layer = 3
                    #先找到该单词
                    word_param=self.words.get(word_name,None)
                    if word_param!=None and layer==len(commond_list):
                        self.Wo.show_words({word_name:word_param})
                        console = Console()
                        table = Table()
                        table.add_column("扩展信息", width=20, overflow="fold")
                        table.add_column("", width=100, overflow="fold")
                        table.add_row("组别", str(self.words[word_name]["group"]))
                        table.add_row("", "")  # 空行
                        if self.words[word_name]["example"] != None:
                            table.add_row("例句1", self.words[word_name]["example"][0])
                            table.add_row("例句2", self.words[word_name]["example"][1])
                            table.add_row("", "")  # 空行
                        if self.words[word_name]["tips"] != None:
                            table.add_row("tips", self.words[word_name]["tips"])
                            table.add_row("", "")
                        console.print(table)
                    elif word_param!=None and (layer)+1==len(commond_list):
                        if util.re_complish(commond_list[layer],"tips"):#tips,example,chines,wid,remove_group,add_group
                            ai=AiObj()
                            print("Wait a moment...")
                            word_param["tips"]=ai.get_tips(word_name)
                            print(f"get '{word_name}' tips succeed!")
                        elif util.re_complish(commond_list[layer],"example"):#tips,example,chines,wid,remove_group,add_group
                            ai = AiObj()
                            print("Wait a moment...")
                            word_param["example"]=ai.get_example(word_name)
                            print(f"get '{word_name}' example succeed!")
                    elif word_param != None and (layer) + 1 <= len(commond_list):
                        #word name word1 [wid] []
                        if util.re_complish(commond_list[layer],"wid"):#tips,example,chines,wid,remove_group,add_group
                            word_param["wid"]=commond_list[layer+1]
                        elif util.re_complish(commond_list[layer],"chines"):#tips,example,chines,wid,remove_group,add_group
                            word_param["chines"]=commond_list[layer+1]
                        elif util.re_complish(commond_list[layer],"remove_group"):#tips,example,chines,wid,remove_group,add_group
                            group_list=commond_list[layer+1:]
                            for i in group_list:
                                if i in word_param["group"]:
                                    word_param["group"].remove(i)
                                    print(f"'{word_name}' remove group <{i}>")
                                else:
                                    print(f"'{word_name}' not in gourp <{i}>")
                        elif util.re_complish(commond_list[layer],"add_group"):#tips,example,chines,wid,remove_group,add_group
                            group_list = commond_list[layer + 1:]
                            for i in group_list:
                                if i not in word_param["group"]:
                                    word_param["group"].append(i)
                                    print(f"'{word_name}' add group <{i}> succeed!")
                                else:
                                    print(f"'{word_name}' is already in group <{i}>")
                        else:
                            print("syntax error")
                    else:
                        print(f"no {word_name} ")
                else:
                    print("参数不足")
            else:
                print("syntax error")

        elif util.re_complish(commond_list[layer],"kong_lib")and commond_len>layer+1:
            layer = 1
        elif util.re_complish(commond_list[layer],"log_lib")and commond_len>layer+1:
            layer = 1
        elif util.re_complish(commond_list[layer],"system")and commond_len>layer+1:
            layer = 1
            if util.re_complish(commond_list[layer],"sd"):
                layer = 2
                if util.re_complish(commond_list[layer],"enable"):
                    config_system["sd_is_work"]=True
                elif util.re_complish(commond_list[layer],"disable"):
                    config_system["sd_is_work"] = False
            elif util.re_complish(commond_list[layer],"tips"):
                layer = 2
                if util.re_complish(commond_list[layer],"enable"):
                    config_system["sd_is_work"]=True
                elif util.re_complish(commond_list[layer],"disable"):
                    config_system["sd_is_work"] = False
            elif util.re_complish(commond_list[layer],"example"):
                layer = 2
                if util.re_complish(commond_list[layer],"enable"):
                    config_system["sd_is_work"]=True
                elif util.re_complish(commond_list[layer],"disable"):
                    config_system["sd_is_work"] = False
        else:
            print("syntax error")
        util.save_json(config_system,config["config_system"])
        self.Wo.save_words(self.words,self.word_path)

    def assign_group_grade(self):
        """
        0~40 bad
        40~80 nobad
        80~99 good
        :return:
        """
        grade=["bad","good","great"]
        for i in self.words:
            word=self.words[i]
            tag=None
            for i in grade:
                if i in word["group"]:
                    tag=i

            if word["accuracy"][2]>=0 and word["accuracy"][2]<0.65:
                if tag==None :
                    word["group"].append("bad")
                else:
                    if tag!="bad":
                        word["group"].remove(tag)
                        word["group"].append("bad")



            elif word["accuracy"][2]>=0.65 and word["accuracy"][2]<0.8:
                if tag == None:
                    word["group"].append("good")
                else:
                    if tag != "good":
                        word["group"].remove(tag)
                        word["group"].append("good")
            elif word["accuracy"][2]>=0.8 and word["accuracy"][2]<=0.99:
                if tag == None:
                    word["group"].append("great")
                else:
                    if tag != "great":
                        word["group"].remove(tag)
                        word["group"].append("great")




