"""
目标：
做一个查找功能（excl）找到在哪天录入的
写入文本的时候每个元素都用换行符隔开
加入一个输错重写功能
合并随机抽查每次随机取全部的20个
要用到叠加函数
做一个写入及时修改的
"""
import functools
import json
import time
from time import sleep
import random
import sys
import pyttsx3
import os

#选区机制及基本必要属性————————————————————————————————————————————————————————————————————————————————————————
esc=1
zhong=3
all_file  = []
w = input("选择记忆类型(danci,duiying):")
if w=="danci":
    c = input("日期:")
elif w=="duiying":
    c = input("打开文件()")
#suiji的全部单词获取————————————————————————————————————
all_file = []
all_world = []
all_world_any =[]

def All_file():#记得要最后清除all_file列表
    for path,disname,file in os.walk("E:\记忆区\danci"):
        for i in file:
            all_file.append(os.path.join(path,i))
    for i in all_file:
        hh = open(i,"r",encoding="utf-8")
        ee= json.loads(hh.read())
        all_world.append(ee.items())
    all_world_list = functools.reduce(lambda a,b:list(a)+list(b),all_world)
    for v in range(20):
        all_world_any.append(random.choice(all_world_list))
    print(dict(all_world_any))
    return dict(all_world_any)



#中英互换——————————————————————————————————————————————————————————————————————————————————————————————————



def zhong1(x):
    global b,zhong
    zhong = int(input("（英译中是：1否：0）:"))
    if zhong==1:
        b = {}
        for i in x:
            b[x[i]] = i
        return b
    else:
        return x
#——————————————————————————————————————————————————————————
#时间包
def sum_time(x):
    def time():
        x()
        end = time.time()
        end_time = time.asctime()
        print(f"开始时间为:{start_time}\n",
              f"结束时间为:{end_time}\n",
              "花费时间:", (end - start) // 60, "分钟")
        time.sleep(5)
    return time

class Xieru():#写入————————————————————————————————————————————————————————————————————————————————————————--

    def xieru(self):
        with open(f"E:/记忆区/{w}/{c}.txt", "a+", encoding="utf-8") as f:
            f.seek(0, 0)
            if f.read(1) == "{":
                f.seek(0, 0)
                everyday = json.loads(f.read())
            else:
                everyday = {}
                f.write(json.dumps(everyday))

        def zhongwen(x):
            if '\u4e00' <= x <= '\u9fa5':
                return 1
            else:
                return 0

        def yingwen(x):
            if '\u4e00' <= x <= '\u9fa5':
                return 0
            else:
                return 1
        geshu = len(everyday)
        xieru1 = 1
        if len(everyday)!=0:
            shangci = everyday.get(list(everyday)[len(everyday)-1])
            print(f"上次写入到{shangci}")
        else:
            pass
        while xieru1 != 00:
            word = input(f"已录{geshu},addword:")
            if word == "00":
                xieru1 = 00
                print("完成写入")
            elif word == "xiugai":
                try:
                    geshu -= 1  # 保持修改的个数不变
                    xiugai = input("输入要修改的词：")
                    everyday.pop(xiugai, "没找到")
                    word = input(f"已录{geshu},修改为:")
                    zhongwen2 = functools.reduce(lambda x, y: x + y, filter(zhongwen, word))#中英分别
                    yingwen2 = functools.reduce(lambda x, y: x + y, filter(yingwen, word))
                    everyday[f"{zhongwen2}"] = f"{yingwen2}"
                    speak(zhongwen2,yingwen2)
                    print(f"已修改为{zhongwen2}:{yingwen2}")
                    geshu+=1
                except TypeError:
                    print("输入不符合格式，重新输入")

            else:
                try:
                    zhongwen2 = functools.reduce(lambda x, y: x + y, filter(zhongwen, word))
                    yingwen2 = functools.reduce(lambda x, y: x + y, filter(yingwen, word))
                    everyday[f"{zhongwen2}"] = f"{yingwen2}"
                    speak(zhongwen2,yingwen2)
                    print(f"已加入{zhongwen2}:{yingwen2}")
                    geshu+=1
                except TypeError:
                    print("输入不符合格式，重新输入")
            with open(f"E:/记忆区/{w}/{c}.txt", "w", encoding="utf-8") as f:
                f.seek(0, 2)  # seek方法是第一个参数是偏移量，第二个参数是位置0是开头，1是当前位置，2是末尾
                shuchu = json.dumps(everyday, ensure_ascii=False)
                f.write(shuchu)
xieru = Xieru()
#测试————————————————————————————————————————————————————————————————————————————————————————————————————————————————
class Ceshi():
    def ceshi(self):
        with open(f"E:/记忆区/{w}/{c}.txt", "r", encoding="utf-8") as f:
            everyday = json.loads(f.read())
        # 判断对错机制，go继续大循环，cishu答题机会，zh每次投出的问题单词
        everyday = zhong1(everyday)
        touchu = iter(everyday)
        go = 1  # 0为退出，1为继续
        cishu = 2  # 2为继续，0为下一个
        shengxia = len(everyday)
        while go == 1:
            cishu = 2
            zh = next(touchu, '今日完成')
            if zh == "今日完成":
                print(zh)
                break
            else:
                shengxia-=1
                speak(zh, everyday[zh])
                danci = input(f"剩下{shengxia}个,{zh}|:")
            while cishu != 0:
                b = zh
                if danci == everyday[b] :
                    print("正确")
                    cishu = 0
                elif danci=="":#跳过暂时的词
                    print(f'正确为:{everyday[b]}')
                    input("默一遍:")
                    print("\n"
                          "\n"
                          "\n"
                          "\n"
                          "\n"
                          "\n"
                          "\n")
                    input("默一遍:")
                    y = list(touchu)  # ————————————————————————————————————————————————————————
                    y.append(b)  # 回收机制
                    touchu = iter(y)  # ————————————————————————————————————————————————————————
                    cishu = 0
                elif danci == "00":
                    print("退出")
                    cishu = 0
                    go = 0
                elif danci != "00" and danci != everyday[b]:
                    speak(b, everyday[b])
                    danci2 = input(f"第二次机会，{b}:")
                    if danci2 == everyday[b]:
                        print("正确")
                        cishu = 0
                    elif danci2 == "00":
                        print("退出")
                        cishu = 0
                        go = 0
                    elif danci2 != "00" and danci2 != everyday[b]:
                        print(f'正确为:{everyday[b]}')
                        input("默一遍:")
                        print("\n"
                              "\n"
                              "\n"
                              "\n"
                              "\n"
                              "\n"
                              "\n")
                        input("默一遍:")
                        y=list(touchu)#————————————————————————————————————————————————————————
                        y.append(b)#回收机制
                        touchu=iter(y)#————————————————————————————————————————————————————————
                        cishu = 0
ceshi = Ceshi()
#随机抽查——————————————————————————————————————————————————————————————————————————————————————————————
class Suiji():
    # ————————抽查算法部分代码——————————————————————————————————————————————————————————————————————————————————————————————————————
    def new_list(self,x):  # 初始化列表
        global eve
        eve = []
        for i in x:
            eve.append([i, 2])
    def lift(self,x):
        for i in eve:
            if i[0] == x :
                i[1] += 2
            else:
                pass
    def right(self,x):
        for i in eve:
            if i[0] == x:
                i[1] -= 1
            else:
                pass
    def eve_next(self,x):#根据积分表展开列表x:积分表
        eve_next=[]
        for i in x:
            for c in range(i[1]):
                eve_next.append(i[0])
        return eve_next
    #————————————————————————————————————————————————————————————————————————————————
    def suiji(self):
        if xuanze =="all_suiji":
            everyday = All_file()
        else:
            with open(f"E:/记忆区/{w}/{c}.txt", "r", encoding="utf-8") as f:
                everyday = json.loads(f.read())
        everyday = zhong1(everyday)
        # 判断对错机制，go继续大循环，cishu答题机会，zh每次投出的问题单词
        everyday_list = list(everyday.keys())
        self.new_list(everyday_list)#初始化列表，积分列表eve
        go = 1  # 0为退出，1为继续
        cishu = 2  # 2为继续，0为下一个
        while go == 1:
            try:
                cishu = 2
                eve_next=self.eve_next(eve)#根据积分表生成展开列表
                touchu = random.choice(eve_next)
                speak(touchu,everyday[touchu])
                #danci = input(f"{touchu}|:")
                while cishu != 0:
                    danci = input(f"{touchu}                           |:")
                    b = touchu
                    if danci == everyday[b]:
                        print("正确")
                        self.right(touchu)
                        cishu = 0
                    elif danci == "00":
                        print("退出")
                        cishu = 0
                        go = 0
                    elif danci=="shengyu":
                        print(len(eve_next))
                    elif danci != "00" and danci != everyday[b]:
                        speak(touchu, everyday[touchu])
                        danci2 = input(f"第二次机会，{b}:")
                        if danci2 == everyday[b]:
                            print("正确")
                            self.right(touchu)
                            cishu = 0
                        elif danci2 == "00":
                            print("退出")
                            cishu = 0
                            go = 0
                        elif danci2 != "00" and danci2 != everyday[b]:
                            print(f'正确为:{everyday[b]}')
                            self.lift(touchu)  # 记录错误函数
                            cishu = 0
            except IndexError:
                end = time.time()
                end_time = time.asctime()
                print(f"开始时间为:{start_time}\n",
                      f"结束时间为:{end_time}\n",
                      "花费时间:", (end - start) // 60, "分钟")
                go = 0
    def no_speek(self):
        with open(f"E:/记忆区/{w}/{c}.txt", "r", encoding="utf-8") as f:
            everyday = json.loads(f.read())
        everyday = zhong1(everyday)
        # 判断对错机制，go继续大循环，cishu答题机会，zh每次投出的问题单词
        everyday_list = list(everyday.keys())
        self.new_list(everyday_list)  # 初始化列表，积分列表eve
        go = 1  # 0为退出，1为继续
        cishu = 2  # 2为继续，0为下一个
        while go == 1:
            try:
                cishu = 2
                eve_next = self.eve_next(eve)  # 根据积分表生成展开列表
                touchu = random.choice(eve_next)
                # danci = input(f"{touchu}|:")
                while cishu != 0:
                    danci = input(f"{touchu}                           |:")
                    b = touchu
                    if danci == everyday[b]:
                        print("正确")
                        self.right(touchu)
                        cishu = 0
                    elif danci == "00":
                        print("退出")
                        cishu = 0
                        go = 0
                    elif danci == "shengyu":
                        print(len(eve_next))
                    elif danci != "00" and danci != everyday[b]:
                        danci2 = input(f"第二次机会，{b}:")
                        if danci2 == everyday[b]:
                            print("正确")
                            self.right(touchu)
                            cishu = 0
                        elif danci2 == "00":
                            print("退出")
                            cishu = 0
                            go = 0
                        elif danci2 != "00" and danci2 != everyday[b]:
                            print(f'正确为:{everyday[b]}')
                            self.lift(touchu)  # 记录错误函数
                            cishu = 0
            except IndexError:
                end = time.time()
                end_time = time.asctime()
                print(f"开始时间为:{start_time}\n",
                      f"结束时间为:{end_time}\n",
                      "花费时间:", (end - start) // 60, "分钟")
                go = 0






#———————初始化声音系统———————————————————————————————————————————————————————————————————————————————————————————————
spk = pyttsx3.init()
spk.setProperty("volume", 1)
spk.setProperty("rate", 170)
def speak(x,y,z="z"):#x是键，y是值
    if zhong ==1:
        spk.say(f"{z},{x}")
        spk.runAndWait()
    elif zhong ==0:
        spk.say(f"{z},{y}")
        spk.runAndWait()
    else:
        spk.say(f"{z},{y},{x}")
        spk.runAndWait()

suiji = Suiji()
start_time = time.asctime()
start = time.time()
while esc==1:
    try:
        with open(f"E:/记忆区/{w}/{c}.txt", "r", encoding="utf-8") as f:
            pass
    except FileNotFoundError:
        print("文件未被创建，只能写入")
        xuanze ="xieru"
    else:
        xuanze = input("（退出:00,写入：xieru，测试：ceshi,随机：suiji,总随机：all_suiji,无声随机：no_speek）  :")
    if xuanze =="00":
        esc=0
        end = time.time()
        end_time = time.asctime()
        print(f"开始时间为:{start_time}\n",
              f"结束时间为:{end_time}\n",
              "花费时间:", (end - start) // 60, "分钟")
        time.sleep(10)
        sys.exit()
    elif xuanze == "xieru":
        xieru.xieru()
    elif xuanze =="ceshi" :
        ceshi.ceshi()
    elif xuanze == "suiji":
        suiji.suiji()
    elif xuanze == "zhong":
        pass
    elif xuanze == "all_suiji":
        suiji.suiji()
    elif xuanze == "no_speek":
        suiji.no_speek()
end = time.time()
end_time= time.asctime()
print(f"开始时间为:{start_time}\n",
        f"结束时间为:{end_time}\n",
        "花费时间:",(end-start)//60,"分钟")





