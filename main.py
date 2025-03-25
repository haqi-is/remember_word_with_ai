from model import Suiji,Ceshi,Xieru,Help,Aichat,Log,Show
import time
from util import show_choies_file,show_title,init_system
from LogObj import LogObj
import os
from config_user import config
from rich.table import Table
from rich.console import Console
if __name__=="__main__":
    # show_title(config["title_image_path"])
    # time.sleep(1)
    # os.system("cls")
    init_system()
    #选区机制及基本必要属性————————————————————————————————————————————————————————————————————————————————————————
    root_path=config["root_path"]
    status=\
        {

        }
    esc=1
    zhong=3
    #提示选库信息
    console=Console()
    title_table=Table()
    title_table.add_column("自定义库")
    title_table.add_column("其他单词库")
    title_table.add_row("<self>","<lib>")
    console.print(title_table)
    #^
    w = input("选择单词库>>>")
    choies_file_name=None
    lib_choies_tag=True
    while w!="quit" and lib_choies_tag==True:
        if w=="self":
            choies_file_name="words.json"
            path = os.path.join(config["root_word_path"],"words.json")
            tip = "私有单词库"
            lib_choies_tag = False
        elif w=="lib":
            choies_file_name=show_choies_file(config["root_word_path"],ftype="filename",choies_type="lib")
            path= os.path.join(config["root_word_path"],choies_file_name)
            tip=choies_file_name
            lib_choies_tag = False
        elif w=="quit":
            exit(0)
        else:
            print("啾咪^~^没有命中单词库哦~")
            w = input("选择单词库>>>")
        os.system("cls")

    print(f"已选择”{tip}“\n\n")
    start_time = time.asctime()
    start = time.time()
    while esc==1:
        try:#检测文件是否存在
            with open(path, "r", encoding="utf-8") as f:
                pass
        except FileNotFoundError:
            print(f"{choies_file_name}文件未被创建，已为您创建成功")
            time.sleep(1)
            xuanze ="write"
            path = os.path.join(config["root_word_path"], choies_file_name)
        else:

            xuanze = input("(help提供帮助)>>>")

        #模式分流
        if xuanze =="quit":
            esc=0
            end = time.time()
            end_time = time.asctime()
            print(f"开始时间为:{start_time}\n",
                  f"结束时间为:{end_time}\n",
                  "花费时间:", (end - start) // 60, "分钟")
        elif xuanze == "help":
            helps=Help()
            helps.pri_menu()
        elif xuanze == "write":
            xieru = Xieru(path,choies_file_name)
            xieru.xieru()
            os.system("cls")
        elif xuanze =="ceshi" :
            ceshi = Ceshi(path,start,start_time)
            ceshi.ceshi(choies_file_name)
            os.system("cls")
        elif xuanze == "suiji":
            suiji = Suiji(path,start,start_time)
            suiji.suiji(choies_file_name)
            os.system("cls")
        elif xuanze == "all_suiji":
            suiji = Suiji(path,start,start_time,xuanze=xuanze)
            suiji.suiji()
            os.system("cls")
        elif xuanze == "ai":
            ai=Aichat()
            ai.aichat_stream()
            os.system("cls")
        elif xuanze == "kong":
            os.system("cls")
            ai=Aichat()
            ai.tiankong(path)
            os.system("cls")
        elif xuanze=="show":
            os.system("cls")
            show=Show(path)
            show.show()
        elif xuanze == "log":
            os.system("cls")
            logobj=Log(path)
            logobj.show_log()
            input("<回车>")
            os.system("cls")
        elif xuanze=="clear":
            os.system("cls")
        elif xuanze=="":
            pass
        else:
            logobj=LogObj(path)
            logobj.commond_control(xuanze,path)
