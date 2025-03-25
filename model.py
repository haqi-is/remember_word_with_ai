import time

import util
from util import All_file,overtime
from WordObj import WordObj as WO
from AiObj import AiObj
from LogObj import  LogObj
from util import show_choies_file,stream_show,from_strs_get_word,show_tips_table
import json
import random
import os
from config_user import config
from rich.table import Table
from rich.console import Console
from  sdObj import sdObj  as SD

class Xieru():#写入————————————————————————————————————————————————————————————————————————————————————————--
    def __init__(self,path,choies_file_name):
        self.path=path
        self.choies_file_name=choies_file_name
    def xieru(self):
        today_tag=util.check_is_today(self.choies_file_name)
        ai = AiObj()
        everyday=None
        with open(self.path, "a+", encoding="utf-8") as f:
            f.seek(0, 0)
            if f.read(1) == "{":#初始化everyday
                f.seek(0, 0)
                everyday = json.loads(f.read())
            else:
                everyday = {}
                f.write(json.dumps(everyday))
        geshu = len(everyday)
        xieru1 = 1

        while xieru1 != "quit":
            os.system("cls")
            if len(everyday) != 0:
                shangci = everyday.get(list(everyday)[len(everyday) - 1])
                heads = ["已录", "上个单词", "输入格式", "例子","提示"]
                raws = [[str(geshu), shangci['word'], "'英文'+'中文'+'组别'", "good棒棒哒;好<adj,good","1.组别为可选项\n2.组别中词性缩写作关键词使用（例v为动词）\n3.如需修改单词重新写入覆盖"]]
                show_tips_table(heads, raws)
            else:
                heads = ["新词库",  "输入格式", "例子","提示"]
                raws = [[" ", "'英文'+'中文'+'词性'", "good棒棒哒;好<adj,good","1.组别为可选项\n2.组别中词性缩写作关键词使用（例v为动词）\n3.如需修改单词重新写入覆盖"]]
                show_tips_table(heads, raws)
            word = input(f">>>")
            wo = WO()

            if word == "quit":
                xieru1 = "quit"
                print("完成写入")
            elif word == "del":
                try:
                    geshu -= 1  # 保持修改的个数不变
                    xiugai = input("输入要删除的词：")
                    everyday.pop(xiugai, "没找到")
                except TypeError:
                    print("输入不符合格式，重新输入")
            else:
                try:
                    set_word_tag=wo.set_word(word)#根据输入的word字符串，如：“sys眼睛”，分给给单词实例对象的word，chines属性进行赋值
                    if set_word_tag!="格式错误":
                        everyday[f"{wo.word}"] = wo.get_word_dict()
                        everyday[f"{wo.word}"]["group"] = [time.strftime("%Y-%m-%d"),today_tag]#换成时间切换函数
                        cixing=util.set_group_cixing(word)
                        if cixing:
                            everyday[f"{wo.word}"]["group"].extend(cixing)
                        everyday[f"{wo.word}"]["first_time"] = time.strftime("%Y-%m-%d_%H:%M:%S")  # 设置首次创建时间
                        everyday[f"{wo.word}"]["last_time"] = time.strftime("%Y-%m-%d_%H:%M:%S")  # 设置最新出现时间
                        geshu += 1
                    else:
                        print(f"write {wo.word} faild! syntax error：未给出英文或翻译")
                        time.sleep(1)

                except TypeError:
                    print("输入不符合格式，重新输入")

        #生成例句
        os.system("cls")
        print("保存分析(生成例句,初始化)单词中。。。")
        for i in everyday:
            example=everyday[i]
            if example["example"]==None:
                example["example"] = ai.get_example(i)
                print("save,",i,f"\n例句：{example['example'][0]}\n{example['example'][1]}\n\n")
        #保存单词文件
        with open(self.path, "w", encoding="utf-8") as f:#向文件写入所有单词
            f.seek(0, 2)  # seek方法是第一个参数是偏移量，第二个参数是位置0是开头，1是当前位置，2是末尾
            shuchu = json.dumps(everyday, ensure_ascii=False,indent=4)
            f.write(shuchu)


#测试————————————————————————————————————————————————————————————————————————————————————————————————————————————————
class Ceshi():
    def __init__(self,path,start,start_time):
        self.path=path
        self.start=start
        self.start_time=start_time
        self.ai = AiObj \
                (
                config["api_key"],
                config["model"],
                config["base_url"]
            )
    def ceshi(self,choies_file_name):
        """

        :param model:{"today":1,"all":2,"batch":strs}
        :return:
        """
        os.system("cls")
        logobj=LogObj(self.path)
        everyday = logobj.words
        # 判断对错机制，go继续大循环，cishu答题机会，zh每次投出的问题单词
        #选择单词的范围
        tips_header=["测试范围","输入","解释"]
        tips_body=[["today","<1>","今日新增的词汇"],
                   ["all","<2>","对本单词库中所有单词库测试"],
                   ["group","直接输入组别名","只测试属于该组别的词汇"],]
        tips_body=tips_body+util.today_batch(choies_file_name)
        show_tips_table(tips_header,tips_body)
        model=input("请选择测试范围>>>")
        if model=="1":
            everyday=logobj.from_group_to_everyday(everyday,tag=time.strftime("%Y-%m-%d"))
        elif model=="2":#所有的单词
            pass
        else:
            everyday = logobj.from_group_to_everyday(everyday, tag=model)
        #^
        if len(everyday)<10:
            print("将会出现这些单词:",*[i for i in everyday.keys()],sep=" | ")
        touchu = iter(everyday)
        go = 1  # 0为退出，1为继续
        shengxia = len(everyday)
        while go == 1:
            os.system("cls")
            cishu = 2
            en=next(touchu, '今日完成')
            logobj.log_add_word(en)
            if en == "今日完成":
                print(en)
                go=0
                cishu=0
            else:
                zh = everyday[en]["chines"]
                if shengxia>0:
                    shengxia-=1
                    shengxia_out=f"剩下{shengxia}个"
                else:
                    shengxia_out="重默刚刚输入错的"
                # speak(zh, everyday[zh])
                danci = input(f"{shengxia_out},{zh}:")
            while cishu != 0:
                b = zh
                if danci == en :
                    print("正确")
                    logobj.set_word_log(en,"right")
                    cishu = 0
                    os.system("cls")
                elif danci=="":#跳过暂时的词
                    # logobj.set_word_log(en, "wrong")
                    print(f'正确为:{en}')
                    input(f"默一遍{zh}:")
                    os.system("cls")
                    input(f"再默一遍{zh}:")
                    y = list(touchu)  # ————————————————————————————————————————————————————————
                    y.append(en)  # 回收机制
                    touchu = iter(y)  # ————————————————————————————————————————————————————————
                    cishu = 0
                elif danci == "quit":
                    print("退出")
                    cishu = 0
                    go = 0
                elif danci != "quit" and danci != en:
                    logobj.set_word_log(en, "wrong")
                    # speak(b, everyday[b])
                    danci2 = input(f"第二次机会，{b}:")
                    if danci2 == en:
                        logobj.set_word_log(en, "right")
                        print("正确")
                        os.system("cls")
                        cishu = 0
                    elif danci2 == "quit":
                        print("退出")
                        cishu = 0
                        go = 0
                    elif danci2 != "quit" and danci2 != en:
                        print(f'正确为:{en}')
                        #为错误的单词添加tips的程序,如果没有tips记录，则流式生成tips
                        word_tips=logobj.words[en]["tips"]
                        if word_tips==None:
                            cmd_output=f'还是答错了,正确为:{en}\n给你来点tips：\t'
                            word_tips=""
                            word_tips_stream=self.ai.get_tips(en,stream=True)
                            for s in word_tips_stream:
                                s = s.choices[0].delta.content
                                cmd_output = stream_show(cmd_output,s)
                                word_tips+=s
                            logobj.words[en]["tips"]=word_tips
                        else:
                            word_tips=word_tips
                            print("tips:\t",word_tips)
                        #^
                        logobj.set_word_log(en, "wrong")

                        input(f"\n默一遍{zh}:")
                        os.system("cls")
                        input(f"再默一遍{zh}:")
                        os.system("cls")
                        y=list(touchu)#————————————————————————————————————————————————————————
                        y.append(en)#回收机制
                        touchu=iter(y)#————————————————————————————————————————————————————————
                        cishu = 0
        else:
            logobj.save_log()
        logobj.assign_group_grade()
        logobj.Wo.save_words(logobj.words,self.path)#这句一定在最后


#随机抽查——————————————————————————————————————————————————————————————————————————————————————————————
class Suiji():
    def __init__(self,path,start,start_time,xuanze=None):
        self.path=path
        self.xuanze=xuanze
        self.start=start
        self.start_time=start_time
        self.ai = AiObj \
                (
                config["api_key"],
                config["model"],
                config["base_url"]
            )
    # ————————抽查算法部分代码——————————————————————————————————————————————————————————————————————————————————————————————————————

    def suiji(self,choies_file_name):
        os.system("cls")

        # everyday = zhong1(everyday)
        # # 判断对错机制，go继续大循环，cishu答题机会，zh每次投出的问题单词
        # everyday_list = list(everyday.keys())
        # self.new_list(everyday_list)#初始化列表，积分列表eve
        logobj = LogObj(self.path)
        everyday=logobj.words
        tips_header = ["测试范围", "输入", "解释"]
        tips_body = [["today", "<1>", "今日新增的词汇"],
                     ["all", "<2>", "对本单词库中所有单词库测试"],
                     ["group", "直接输入组别名", "只测试属于该组别的词汇"], ]
        tips_body = tips_body + util.today_batch(choies_file_name)
        show_tips_table(tips_header, tips_body)
        model = input("请选择测试范围>>>")
        if model == "1":
            everyday = logobj.from_group_to_everyday(everyday, tag=time.strftime("%Y-%m-%d"))
        elif model == "2":  # 所有的单词
            pass
        else:
            everyday = logobj.from_group_to_everyday(everyday, tag=model)
        # ^
        Wo=WO()
        eve=Wo.create_eve(everyday)
        go = 1  # 0为退出，1为继续

        while go == 1:
            try:
                cishu = 2
                # eve_next=self.eve_next(eve)#根据积分表生成展开列表
                en = random.choice(eve)
                zh=everyday[en]['chines']
                logobj.log_add_word(en)
                # speak(touchu,everyday[touchu])
                #danci = input(f"{touchu}|:")
                while cishu != 0:
                    os.system("cls")
                    danci = input(f"{zh}:")
                    if danci == en:
                        print("正确")
                        logobj.set_word_log(en,"right")
                        eve.remove(en)
                        cishu = 0
                    elif danci == "quit":
                        print("退出")
                        cishu = 0
                        go = 0
                    elif danci=="shengyu":
                        print(len(eve))
                    elif danci != "quit" and danci != en:
                        # speak(touchu, everyday[touchu])
                        logobj.set_word_log(en, "wrong")
                        danci2 = input(f"第二次机会，{everyday[en]['chines']}:")
                        if danci2 == en:
                            print("正确")
                            logobj.set_word_log(en,"right")
                            eve.remove(en)
                            cishu = 0
                        elif danci2 == "quit":
                            print("退出")
                            cishu = 0
                            go = 0
                        elif danci2 != "quit" and danci2 != en:
                            print(f'正确为:{en}')
                            # 为错误的单词添加tips的程序,如果没有tips记录，则流式生成tips
                            word_tips = logobj.words[en]["tips"]
                            if word_tips == None:
                                cmd_output = f'还是答错了,正确为:{en}\n给你来点tips：\t'
                                word_tips = ""
                                word_tips_stream = self.ai.get_tips(en, stream=True)
                                for s in word_tips_stream:
                                    s = s.choices[0].delta.content
                                    cmd_output = stream_show(cmd_output, s)
                                    word_tips += s
                                logobj.words[en]["tips"] = word_tips
                            else:
                                word_tips = word_tips
                                print("tips:\t", word_tips)
                            # ^
                            logobj.set_word_log(en, "wrong")
                            input(f"\n默一遍{zh}:")
                            os.system("cls")
                            eve.extend([en,en])  # 添加一次该元素
                            cishu = 0
            except IndexError:
                overtime(self.start,self.start_time)
                go = 0
        else:
            logobj.save_log()
        logobj.assign_group_grade()
        logobj.Wo.save_words(logobj.words,self.path)#这句一定在最后

    def no_speek(self):
        pass

class Aichat():
    def __init__(self,path="./chat_lib",config=config):
        self.path=path
        self.aiobj=AiObj\
            (
                config["api_key"],
                config["model"],
                config["base_url"]
            )
    def aichat(self):
        """
        非流式输出的问答程序，可用于后台分析
        :return:
        """
        messages_path=show_choies_file(self.path,choies_type="ai")
        history=self.get_history(messages_path)
        os.system("cls")
        print(history)
        input_content = input("提问:")
        while input_content!="quit":
            result= self.aiobj.echo_chat(messages_path,input_content)
            print(self.aiobj.get_content(result))
            input_content = input("提问:")

    def aichat_stream(self):
        """
        流式输出的问答程序，可用实时对话
        :return:
        """
        os.system("cls")
        messages_path=show_choies_file(self.path,choies_type="ai")
        os.system("cls")
        history = self.get_history(messages_path)
        print(history)
        input_content = input(">>>提问:")
        messages=self.aiobj.load_messages(messages_path)

        while input_content!="quit":
            self.aiobj.set_messages(messages, role="user", content=input_content)
            result= self.aiobj.ai_request(messages,stream=True)
            history += f">>>提问:{input_content}\n"
            full_content = ""
            cmd_output= f">>>提问:{input_content}\n"
            for chunk in result:
                s = chunk.choices[0].delta.content
                full_content += s
                cmd_output=stream_show(cmd_output, s)

            self.aiobj.set_messages(messages, role="assistant", content=full_content)
            self.aiobj.save_messages(messages_path,messages)
            os.system("cls")
            history+=(full_content+f"\n\n\n\n")
            print(history)
            input_content = input(">>>提问:")
    def aichat_stream_2(self):
        """
        流式输出的问答逻辑，这个是最初版本，会产生cmd闪烁
        :return:
        """
        os.system("cls")
        messages_path=show_choies_file(self.path,choies_type="ai")
        history = self.get_history(messages_path)
        print(history)
        input_content = input("提问:")
        messages=self.aiobj.load_messages(messages_path)

        while input_content!="quit":
            self.aiobj.set_messages(messages, role="user", content=input_content)
            result= self.aiobj.ai_request(messages,stream=True)
            history += f"提问:{input_content}\n"
            full_content = ""
            for chunk in result:
                s = chunk.choices[0].delta.content
                full_content += s
                history=stream_show(history, s)

            self.aiobj.set_messages(messages, role="assistant", content=full_content)
            self.aiobj.save_messages(messages_path,messages)
            input_content = input("提问:")
    def tiankong(self,path):
        """
        根据单词生成填空文章
        :param path:
        :return:
        """
        print("您需要根据什么生成文章，\n\t.单词库中随即选取单词生成，请<回车>。\n\t.自选单词生成文章,输入格式为<word1 word2 word3>")
        tiankong_xuanze=input(">>>")
        if tiankong_xuanze=="":
            Wo = WO()
            words = Wo.load_words(path)
            words_list=list(words.keys())
            words_choies_list=[]
            for i in range(10):
                words_choies_list.append(random.choice(words_list))
            words_strs = ",".join(words_choies_list)
            system_content="你是一个英语老师，你要考我英语的填空题，会给你几个单词，然后你根据这几个单词写一篇短文,你可以对这些单词改变时态，但一定要符合语法，短文的内容要符合如下原则，必为完全覆盖所有原则但一定至少要满足一点：1.有深意的人生哲理，2.切入角度新颖，3.不要讲儿童故事，4.可以改变真实事件。并用[    ]来提示要填空的位置，但一定不用给出每个空的正确答案，要求生成的短文有趣而且有逻辑,你只需要给出生成的短文，不需要过多的解释"
        else:
            words_list=from_strs_get_word(tiankong_xuanze)
            words_strs = ",".join(words_list)
            system_content="你是一个英语老师，你要考我英语的填空题，会给你几个单词，然后你根据这几个单词写一篇短文,每个词语都需要出现，一定要符合正确的语法，短文的内容要符合如下原则，必为完全覆盖所有原则但一定至少要满足一点：1.有深意的人生哲理，2.切入角度新颖，3.不要讲儿童故事，4.可以改变真实事件。并用[    ]来提示要填空的位置，但一定不用给出每个空的正确答案，要求生成的短文有趣而且有逻辑,你只需要给出生成的短文，不需要过多的解释"
        os.system("cls")
        output_strs=""
        content=words_strs
        messages = [
            {"role": "system",
             "content": system_content},
            {"role": "user", "content": content},  # 需要用于造句的单词
        ]
        print("生成中。。。")
        result1=self.aiobj.ai_request(messages)
        answer1=self.aiobj.get_content(result1)
        output_strs+=f"{answer1}\n"
        os.system("cls")
        print(output_strs)
        tag=input("答案<回车>:")
        print("回答中。。。")
        messages = [
            {"role": "system",
             "content": system_content},
            {"role": "user", "content": content},  # 需要用于造句的单词
            {"role": "assistant", "content": answer1},
            {"role": "user",
             "content": "请你把填空位置的正确的答案告诉我，恳求你语法一定要正确，不需要解释任何东西，按这个格式返回1.word1,2.word2,3.word3"},
        ]
        result2=self.aiobj.ai_request(messages)
        answer2=self.aiobj.get_content(result2)
        os.system("cls")
        output_strs+=f"\n\n参考答案为:{answer2}"
        print(output_strs)
        input("退出<回车>:")
        #保存文件
        with open(f"./kong_lib/{time.strftime('%Y-%m-%d_%H_%M')}.json","w",encoding="utf-8") as f:
            save_tamp={
                "article":answer1,
                "answer":answer2
            }
            save_tamp = json.dumps(save_tamp, ensure_ascii=False, indent=4)
            f.seek(0,2)
            f.write(save_tamp)

    def get_history(self,messages_path):
        strs = ""
        with open(messages_path, "r", encoding="utf8") as f:
            message_history_list = json.load(f)
            for i in message_history_list:
                if i["role"] == "user":
                    strs += f'>>>提问：{i["content"]}\n'
                elif i["role"] == "assistant":
                    strs += f'{i["content"]}\n\n\n\n\n'
        return strs

class Log():
    """

    """
    def __init__(self,path):
        self.path=path
    def show_log(self):
        logobj=LogObj(self.path)
        word_table=logobj.load_log()["word_table"]
        os.system("cls")
        logobj.show_log(word_table)
class Show():
    def __init__(self,path):
        self.path=path
    def show(self):
        Wo = WO(path=self.path)
        words=Wo.load_words()
        words_list=list(words.items())
        max_num=len(words_list)
        zhizhen=0
        show_xuanze=""#[l,"",word,quit]
        while zhizhen<max_num and show_xuanze!=quit:
            os.system("cls")
            rear=zhizhen+10
            if max_num-zhizhen<10:
                rear = max_num
            batch_words=dict(words_list[zhizhen:rear])
            Wo.show_words(batch_words)
            zhizhen+=10
            #提示操作
            console = Console()
            table = Table()
            table.add_column("上一页")
            table.add_column("下一页")
            table.add_column("查单词（直接输入单词）")
            table.add_column("退出")
            table.add_row("<l>","<回车>","<word>","<quit>")
            console.print(table)
            show_xuanze=input(">>>")
            #^
            if show_xuanze=="":
                continue
            elif show_xuanze=="l":
                zhizhen-=20
            elif show_xuanze=="quit":
                os.system("cls")
                break
            else:
                check_word=words.get(show_xuanze,"未找到")
                if check_word=="未找到":
                    input("提示:未找到该单词<回车>")
                    zhizhen-=10
                else:
                    sd = SD()
                    tag_picture = True
                    while tag_picture == True:
                        os.system("cls")
                        Wo.show_words({show_xuanze: check_word})
                        console = Console()
                        table = Table()
                        table.add_column("扩展信息", width=20, overflow="fold")
                        table.add_column("", width=100, overflow="fold")
                        table.add_row("组别", str(words[show_xuanze]["group"]))
                        table.add_row("", "")#空行
                        if words[show_xuanze]["example"] != None:
                            table.add_row("例句1", words[show_xuanze]["example"][0])
                            table.add_row("例句2", words[show_xuanze]["example"][1])
                            table.add_row("", "")#空行
                            # print(f'\n简单句：\n\t{words[show_xuanze]["example"][0]}\n'
                            #       f'复合句：\n\t{words[show_xuanze]["example"][1]}',end="\n\n")
                        if words[show_xuanze]["tips"] != None:
                            table.add_row("tips", words[show_xuanze]["tips"])
                            table.add_row("", "")
                            # print("tips:\n\t",words[show_xuanze]["tips"])
                        console.print(table)

                        picture_xuanze = input("<p>,<回车>")

                        if picture_xuanze == "p":
                            sd.txt_to_img(show_xuanze)

                        else:
                            tag_picture = False

                    else:
                        zhizhen -= 10#抵消之前的zhizhen+=10
        else:
            os.system("cls")




class Help():
    def __init__(self):
        pass
    def pri_menu(self):
        print("\nHelp for you:")
        print(f"\t{'.返回'.ljust(30+6)}<quit>\n"
              f"\t{'.写入单词'.ljust(30+4)}<write>\n"
              f"\t{'.查看单词'.ljust(30+4)}<show>\n"
              f"\t{'.测试所有单词'.ljust(30+2)}<ceshi>\n"
              f"\t{'.抽查单词'.ljust(30+4)}<suiji>\n"
              f"\t{'.AI对话'.ljust(30+6)}<ai>\n"
              f"\t{'.单词填空'.ljust(30+4)}<kong>\n"
              f"\t{'.日志分析'.ljust(30+4)}<log>\n")
    def pri_commond_help(self):
        """
                commond_list={
                    "word":{
                        "group":{
                            "create":"(输入组名)创建一个新组",
                            "remove":"(输入组名)删除一个组，并移出组内单词",
                            "(输入组名)":{
                                "add":"(输入单词1 单词2 单词3)可多选，往组内添加指定单词",
                                "remove":"(输入单词1 单词2 单词3可多选，往组内移除指定单词)",
                                "show":"查看改组单词有哪些"
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
                            },
                        "delete":"[输入单词1、单词2]可多选，批量删除单词",
                        "add":"[输入单词1、单词2]可多选，批量新增单词,需按格式输入"
                            }
                    },
                    "kong_lib":{},
                    "log_lib":{},
                    "system":{
                        "sd":"(输入enable或disable)允许生图，此处并不是开启关闭sd，只是指定在sd启动的情况下，是否进行生图，sd仍然要手动启动",
                        "tips":"(输入enable或disable)是否允许生成tips",
                        "example:"(输入enable或disable)是否允许生成example"

                        }
                }
                :return:
                """