import re
from WordObj import WordObj as WO
from AiObj import AiObj
from sdObj import sdObj
import csv
import functools
import json
import time
import random
import os
from config_user import config
from PIL import Image
from rich.console import Console
from rich.table import Table
import cv2

def All_file(path):
    """
    抽取所有文件中的部分单词
    :param path:
    :return:
    """
    all_file = []
    all_world = []
    all_world_any = []
    for path,disname,file in os.walk(os.path.split(path)[0]):
        for i in file:
            all_file.append(os.path.join(path,i))
    for i in all_file:
        hh = open(i,"r",encoding="utf-8")
        ee= json.loads(hh.read())
        all_world.append(ee.items())
    all_world_list = functools.reduce(lambda a,b:list(a)+list(b),all_world)
    for v in range(20):
        all_world_any.append(random.choice(list(all_world_list)))
    print(dict(all_world_any))
    return dict(all_world_any)


# def show_choies_file(path,ftype="abs",choies_type="common"):
#     """
#     展示一个文件夹内的所有文件，并根据序号返回一个绝对路径，或者文件名，这要根据ftype的值确定
#     :param path: 待遍历文件的根目录
#     :param ftype:"abs"返回选择目录的绝对路径，“filename”返回选择目录的文件名包括后缀
#     :choies_type:
#     :return:str  绝对路径或文件名
#     """
#     file_list = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path,i))]
#     enumerate_file_list=enumerate(file_list,1)
#     for num,file in enumerate_file_list:
#         print(str(num) + ".", file.split(".")[0])
#     if choies_type=="ai":
#         print("(如果创建,请直接命名)")
#     choies_str=input("选择序号或输入:")
#     file_path=""
#     choies=None
#     try:
#         choies=int(choies_str)
#
#     except:
#         if choies_type=="common":
#             file_path = os.path.join(os.path.abspath(path), f"{choies_str}.json")
#         elif choies_type=="ai":
#             print(f"'{choies_str}'会话创建成功")
#             file_path=os.path.join(path,f"{choies_str}.json")
#             with open(file_path,"w",encoding="utf8") as f:
#                 json.dump([{'role': 'system', 'content': '你是一个说话简洁精炼,且不会讨好人，实事求是的助手'}],f)
#             file_path=os.path.join(os.path.abspath(path), f"{choies_str}.json")
#     else:
#         if ftype=="abs":
#             file_path = os.path.join(os.path.abspath(path), file_list[choies-1])
#         elif ftype=="filename":
#             file_path = file_list[choies-1]
#
#     return file_path

def show_choies_file(path,ftype="abs",choies_type="common"):
    """
    展示一个文件夹内的所有文件，并根据序号返回一个绝对路径，或者文件名，这要根据ftype的值确定
    :param path: 待遍历文件的根目录
    :param ftype:"abs"返回选择目录的绝对路径，“filename”返回选择目录的文件名包括后缀
    :choies_type:
    :return:str  绝对路径或文件名
    """
    file_list = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path,i))]
    enumerate_file_list=enumerate(file_list,1)
    for num,file in enumerate_file_list:
        print(str(num) + ".", file.split(".")[0])
    if choies_type=="ai" or choies_type=="lib":
        print("(如果创建,请直接命名)")

    file_path=""
    choies=None
    dayu_choies=True
    while dayu_choies:
        choies_str = input("选择序号或输入:")
        try:
            choies=int(choies_str)

        except:
            if choies_type=="common" or choies_type=="lib":
                file_path = f"{choies_str}.json"#os.path.join(os.path.abspath(path), f"{choies_str}.json")

            elif choies_type=="ai":
                print(f"'{choies_str}'会话创建成功")
                file_path=os.path.join(path,f"{choies_str}.json")
                with open(file_path,"w",encoding="utf8") as f:
                    json.dump([{'role': 'system', 'content': '你是一个说话简洁精炼,且不会讨好人，实事求是的助手'}],f)
                file_path=os.path.join(os.path.abspath(path), f"{choies_str}.json")
            dayu_choies = False
        else:
            if choies<=len(file_list):
                dayu_choies=False
                if ftype=="abs":
                    file_path = os.path.join(os.path.abspath(path), file_list[choies-1])
                elif ftype=="filename":
                    file_path = file_list[choies-1]
            else:
                print("序号不在可选范围内")

    return file_path



# def histroy_strs(stream_strs):
#     strs=""
#     with open("./chat_lib/messages.json","r",encoding="utf8") as f:
#         message_history_list=json.load(f)
#         for i in message_history_list:
#             if i["role"]=="user":
#                 strs+=f'提问：{i["content"]}\n'
#             elif i["role"]=="assistant":
#                 strs+=f'{i["content"]}\n\n'
#         print(strs)
def stream_show(strs,s):
    os.system("cls")
    strs+=s
    print(strs)
    return strs


def from_strs_get_word(strs):
    ying_compile = re.compile("[a-zA-Z]+")
    yingwen = re.findall(ying_compile, strs)
    return yingwen
def csv_to_word_json(csv_path):
    """
    该方法是为例从csv文件中获取数据得到单词words的json文件
    ## 数据格式

    采用 CSV 文件存储所有词条数据，用 UTF-8 进行编码，用 Excel 的话，别直接打开，否则编码是错的。在 Excel 里选择数据，来自文本，然后设定逗号分割，UTF-8 编码即可。

    | 字段        | 解释                                                       |
    | ----------- | ---------------------------------------------------------- |
    | word        |i[0] 单词名称                                                   |
    | phonetic    |i[1] 音标，以英语英标为主                                       |
    | definition  |i[2] 单词释义（英文），每行一个释义                             |
    | translation |i[3] 单词释义（中文），每行一个释义                             |
    | pos         |i[4] 词语位置，用 "/" 分割不同位置                              |
    | collins     |i[5] 柯林斯星级                                                 |
    | oxford      |i[6] 是否是牛津三千核心词汇                                     |
    | tag         |i[7] 字符串标签：zk/中考，gk/高考，cet4/四级 等等标签，空格分割 |
    | bnc         |i[8] 英国国家语料库词频顺序                                     |
    | frq         |i[9] 当代语料库词频顺序                                         |
    | exchange    |i[10] 时态复数等变换，使用 "/" 分割不同项目，见后面表格          |
    | detail      |i[11] json 扩展信息，字典形式保存例句（待添加）                  |
    | audio       |i[12] 读音音频 url （待添加）                                    |
    :param path:
    :return:
    """

    words = {}
    num = 1
    json_path = os.path.join("./word", f"{os.path.basename(csv_path).split('.')[0]}_{num}.json")
    Wo = WO(path=json_path)
    count=0
    with open(csv_path,"r",encoding="utf-8") as f:
        reader=csv.reader(f)
        for i in reader:
            if count==1000:
                json_path = os.path.join("./word", f"{os.path.basename(csv_path).split('.')[0]}_{num}.json")
                Wo = WO(path=json_path)
                Wo.save_words(words, path=json_path)
                count=0
                num+=1
                words={}

            word=i[0]
            chines=i[3]
            word_param=Wo.get_word_dict()
            word_param["word"]=word
            word_param["chines"]=chines
            word_param["accuracy"]=[1,1,0.99]
            word_param["first_time"]=time.strftime("%Y-%m-%d_%H:%M")
            word_param["last_time"] =time.strftime("%Y-%m-%d_%H:%M")
            count+=1
            words[word]=word_param#把单词属性添加到words



def json_to_json(root_path):
    """
    将指定json文件中内容转换成另一种数据格式的json文件
    :param root_path: 指定待json文件的父目录
    :return: None
    """
    num = 0
    for file in os.listdir(root_path):
        if os.path.isfile(os.path.join(root_path,file)):
            words = {}
            json_path = os.path.join(root_path,file)
            Wo = WO(path=json_path)
            with open(json_path, "r", encoding="utf-8") as f:
                src_words=json.load(f)#list
                for i in src_words:
                    num+=1
                    word = i["word"]
                    chines = i["mean"]
                    word_param = Wo.get_word_dict()
                    word_param["word"] = word
                    word_param["chines"] = chines
                    word_param["accuracy"] = [1, 1, 0.99]
                    word_param["first_time"] = time.strftime("%Y-%m-%d_%H:%M")
                    word_param["last_time"] = time.strftime("%Y-%m-%d_%H:%M")
                    words[word] = word_param  # 把单词属性添加到words
            Wo.save_words(words,os.path.join(root_path,"json_word",file))
    print(num)
def unite_json_words(root_path,is_save=False):
    """
    把目录下words_json文件内容合并
    :param root_path: 需要合并json文件所在目录
    :param is_save: [False True]默认只是合并json文件的内容返回合并后的words，也可以选择保存
    :return: 返回合并后的words字典
    """

    words={}
    des_path=os.path.join(root_path,"unitl.json")
    for file in os.listdir(root_path):
        if os.path.isfile(os.path.join(root_path,file)):
            json_path = os.path.join(root_path, file)
            with open(json_path, "r", encoding="utf-8") as f:
                src_words = json.load(f)
                words=dict(list(words.items())+list(src_words.items()))
    if is_save==True:
        with open(des_path,"w",encoding="utf-8") as f:
            f.seek(0,2)
            words=json.dumps(words,indent=4)
            f.write(words)
        print("save succeed")
    return words

def init_first_time(path):
    """
    将字典中每个单词的first_time，last_time初始化成当前时间
    :param path: 单词字典路径
    :return:
    """
    with open(path, "r", encoding="utf-8") as f:
        words = json.load(f)
        for i in words:
            words[i]["first_time"]=time.strftime("%Y-%m-%d_%H:%M:%S")
            words[i]["last_time"] = time.strftime("%Y-%m-%d_%H:%M:%S")
    with open(path, "w", encoding="utf-8") as f:
        f.seek(0, 2)  # seek方法是第一个参数是偏移量，第二个参数是位置0是开头，1是当前位置，2是末尾
        shuchu = json.dumps(words, ensure_ascii=False, indent=4)
        f.write(shuchu)
    print("save succeed")
def init_example(path):
    """
    为单词字典中没有例子的单词初始化例子
    :param path: 单词字典的
    :return:
    """
    api_key = config["api_key"]
    model = config["model"]
    base_url = config["base_url"]
    ai=AiObj(api_key=api_key,
                 model=model,
                 base_url=base_url)
    words = None
    with open(path, "r", encoding="utf-8") as f:
        words = json.load(f)

    with open(path, "w", encoding="utf-8") as f:
        for i in words:
            words[i]["example"] = ai.get_example(i)
            with open(path, "w", encoding="utf-8") as f:
                f.seek(0, 2)  # seek方法是第一个参数是偏移量，第二个参数是位置0是开头，1是当前位置，2是末尾
                shuchu = json.dumps(words, ensure_ascii=False, indent=4)
                f.write(shuchu)
                print(i, "succee")
def show_title(image_path,width=100):
    ascii_chars = '''@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft|()1{}[]?-_+~<>i!lI;:,"^`'. '''  # "█■▣#▪+=▫-. "  # 至少包含 11 个字符"█▩▦▣▪▫    "
    image = Image.open(image_path).convert("L")  # 确保是灰度图
    aspect_ratio = image.height / image.width
    new_height = int(aspect_ratio * width * 0.55)
    image = image.resize((width, new_height))
    pixels = image.getdata()
    scale_factor = len(ascii_chars) - 1
    # ascii_str = "".join([ascii_chars[pixel // (256 // scale_factor)] for pixel in pixels])
    ascii_str = "".join([ascii_chars[min(int(pixel / (255 / scale_factor)), scale_factor)] for pixel in pixels])
    ascii_lines = [ascii_str[i:i + width] for i in range(0, len(ascii_str), width)]

    console = Console()
    ascii_art = ascii_lines
    for line in ascii_art:
        console.print(line)
def show_title_2(img_path):
    from PIL import Image
    import numpy as np

    char_list = '''@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. '''

    def get_char(gray_pix):

        length = len(char_list)  # 确定字符串长度
        unit = 256.0 / length  # 分配每个字符占据的灰度值段
        return char_list[int((((length - 1) * gray_pix)) / 256.0)]  # 对应灰度值与字符

    img_path = img_path
    img = Image.open(img_path)
    img_widht = img.size[0]
    img_height = img.size[1]
    # 缩放图片（因为有些图片太大所以需要缩放
    img = img.resize((int(img_widht * 0.1), int(img_height * 0.1)), Image.NEAREST)
    img_gray = np.array(img.convert('L'), 'f')  # 彩色图转灰度图

    # 创建文本文档并在相对应的位置写入对应字符
    text = " "
    for i in range(int(img_height * 0.1)):
        for j in range(int(img_widht * 0.1)):
            text = text + get_char(img_gray[i, j])
        text = text + '\n'
    print(text)

    text_name = "str_image2" + ".txt"
    return text_name
def show_tips_table(head,row):
    console=Console()
    table=Table()
    for i in head:
        table.add_column(i)
    for i in row:
        table.add_row(*i)
    console.print(table)

def mp4_to_images(video_path,output_path):


    # 视频文件路径
    video_path = video_path
    # 输出目录
    output_dir = output_path

    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 加载视频
    cap = cv2.VideoCapture(video_path)

    frame_number = 0
    while True:
        # 读取下一帧
        ret, frame = cap.read()

        # 如果读取成功
        if ret:
            frame_number += 1
            h, w = frame.shape[:2]  # 获取当前帧的尺寸

            # 计算裁剪的起始点
            start_x = max(0, w // 2 - 400)  # 宽度中心减去一半的目标宽度
            start_y = max(0, h // 2 - 250)  # 高度中心减去一半的目标高度

            # 裁剪帧到800x500
            cropped_frame = frame[start_y:start_y + 500, start_x:start_x + 800]  # 修改这里的高度为500

            # 保存裁剪后的帧到文件
            frame_filename = os.path.join(output_dir, f"frame_{frame_number:04d}.jpg")
            cv2.imwrite(frame_filename, cropped_frame)
        else:
            break

    # 释放资源
    cap.release()

def init_group(path=None,group=[]):
    Wo=WO(path)
    words=Wo.load_words(path)
    for i in words:
        words[i]["group"]=group
    Wo.save_words(words,path)
def check_is_today(choies_file_name):
    today=time.strftime("%Y-%m-%d")
    today_temp =None
    with open("./temp/today_add_group.json",mode="r",encoding="utf-8") as f:
        today_temp=json.load(f)
        #如果不存在缓存则初始化
        file_name=today_temp.get(choies_file_name,False)
        if file_name==False:
            today_temp[choies_file_name]={"num":1,"tag":today}
        else:
            if today_temp[choies_file_name]["tag"]!=today:
                today_temp[choies_file_name]["num"]=1
                today_temp[choies_file_name]["tag"]=today
            else:
                today_temp[choies_file_name]["num"] += 1
    with open("./temp/today_add_group.json", mode="w", encoding="utf-8") as f:
        f.seek(0, 2)  # seek方法是第一个参数是偏移量，第二个参数是位置0是开头，1是当前位置，2是末尾
        shuchu = json.dumps(today_temp, ensure_ascii=False, indent=4)
        f.write(shuchu)
    return f"{today}-{today_temp[choies_file_name]['num']}"

def today_batch(choies_file_name):
    group_temp_path=f"./temp/today_add_group.json"
    today_time=time.strftime("%Y-%m-%d")
    today_group_list=[]
    with open(group_temp_path,mode="r",encoding="utf-8") as f:
        group_temp = json.load(f)
        if today_time==group_temp[choies_file_name]["tag"]:
            batch_num=group_temp[choies_file_name]["num"]
            today_group_list.append(["", "", ""])
            today_group_list.append([f"以下为今日新增", "", ""])
            for i in range(1,batch_num+1):
                today_group_list.append([f"第{i}批",f"{today_time}-{i}",f"测试第{i}批新增词汇"])
        return today_group_list

def set_group_cixing(strs):
    cixing_compile = re.compile("[<《]([^>》]+)")#[>》]
    cixing = re.search(cixing_compile, strs)
    if cixing!=None:
        cixing = cixing.group(1).split("，")
    else:
        cixing=""
    cixing_end=[]#n，j,l
    for i in cixing:
        cixing_end.extend(i.split(","))
    if len(cixing_end)!=0:
        return cixing_end
    else:
        return False




def overtime(start,start_time):
    end = time.time()
    end_time = time.asctime()
    print(f"开始时间为:{start_time}\n",
          f"结束时间为:{end_time}\n",
          "花费时间:", (end - start) // 60, "分钟")

def save_json(content,path):
    with open(path,"w",encoding="utf-8") as f:
        f.seek(0, 2)  # seek方法是第一个参数是偏移量，第二个参数是位置0是开头，1是当前位置，2是末尾
        shuchu = json.dumps(content, ensure_ascii=False, indent=4)
        f.write(shuchu)
def load_json(path):
    content=None
    with open(path,"r",encoding="utf-8") as f:
        content=json.load(f)
    return content
def re_complish(content,complish):
    complates=re.compile(f"^{content}")
    result = re.search(complates,complish)
    if result:
        return True
    else:
        # print(f"syntax error:no match:{content},is {complish}?")
        return False

def init_system():
    os.system("cls")
    print("char_ai:配置自检...")
    try:
        from AiObj import AiObj
        ai = AiObj()
        init_messages=ai.set_messages([])
        ai.ai_request(messages=init_messages)
    except:
        print("char_ai:未配置或配置错误")
        input("请完成char_ai的配置后重启程序")
        exit(0)
    else:
        print("char_ai:正常.")

    print("sd:配置自检...")
    try:
        sd=sdObj()
        with open("config_system.json","r",encoding="utf-8") as f:
            config_system=json.load(f)
        if config_system["sd_is_work"]==True and sd.check_sd_enable()==True:
            print("sd:正常")
        elif sd.check_sd_enable()==True:
            print("sd:生图引擎已关闭,此为可选项不影响其他功能的使用(检测到本地sd已启动,但配置文件config_system.json中sd_is_work为false,设置值为true并重启来启动)")
        else:
            print("sd:未启动,但不影响其他功能的使用.")

    except:
        print("sd:未启动或未配置成功,如果sd正确启动(需要自行安装sd)但未生效,则请定位到config_system.json中将sd_is_work设置为true")
        config_system["sd_is_work"] = False
        with open("config_system.json","w",encoding="utf-8") as f:
            f.seek(0, 2)  # seek方法是第一个参数是偏移量，第二个参数是位置0是开头，1是当前位置，2是末尾
            config_system = json.dumps(config_system, ensure_ascii=False, indent=4)
            f.write(config_system)
    input("回车>>>")
    os.system("cls")





