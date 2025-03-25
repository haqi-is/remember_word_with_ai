from config_user import config
import os
from openai import OpenAI
import json



#测试属性


class AiObj():
    def __init__(self,
                 api_key=config["api_key"],
                 model=config["model"],
                 base_url=config["base_url"]
                 ):
        self.api_key=api_key
        self.model=model
        self.base_url=base_url
    def ai_request(self,messages,stream=False):
        client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )
        completion = client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=stream
        )
        if stream==False:
            result=completion.model_dump_json()
            result=json.loads(result)
        else:
            result=completion
        return result
    def set_messages(self,messages,role="user",content=""):
        """
        :param messages:
        :param role: ["system","user","assistant"]
        :param content:
        :return:
        """
        if len(messages)==0:
            messages.append({'role': 'system', 'content': '你是一个说话简洁精炼,且不会讨好人，实事求是的助手'})
        else:
            messages.append({'role':role,'content':content})
        return messages
    def save_messages(self,path,messages=[]):
        with open(path, "w", encoding="utf-8") as f:
            f.seek(0, 2)  # seek方法是第一个参数是偏移量，第二个参数是位置0是开头，1是当前位置，2是末尾
            messages_json = json.dumps(messages, ensure_ascii=False, indent=4)
            f.write(messages_json)
    def load_messages(self,path):
        messages=[]
        if os.path.exists(path)==False:
            with open(path,"w",encoding="utf8") as f:
                self.set_messages(messages)
                self.save_messages(path,messages)
        with open(path,"r",encoding="utf8") as f:
            messages = json.load(f)
        return messages
    def get_content(self,result):
        return result['choices'][0]["message"]["content"]
    def echo_chat(self,messages_path,input_content):
        messages = self.load_messages(messages_path)
        self.set_messages(messages,
                          role="user",
                          content=input_content)
        result= self.ai_request(messages)
        self.set_messages(messages,
                          role="assistant",
                          content=self.get_content(result))
        self.save_messages(messages_path, messages)
        return result
    def get_tips(self,word,stream=False):
        tips = ""
        message = [
            {"role":"system","content":"你是一个英语老师，我将给你一个单词，返回这个单词的记忆方法，如果没有方法则请说说你对这个单词的理解，加深我对这个单词的记忆程度，我总是记不住这个单词，请用中文解释，请不要说客套话，越是简洁易记最佳"},
            {"role":"user","content":word}
        ]

        result = self.ai_request(message,stream=stream)
        if stream==False:
            tips = self.get_content(result)
        else:
            tips=result
        return tips
    def get_example(self,word):
        message=[
            {"role":"system","content":"你是一个英语老师，我将给你一个单词，你给我这个单词的例句，请给我两个例句，第一个是简单句，第二个是长句，以这样的格式返回给我1.句子1，2.句子2，与举例无关的客套话不要说，我只要你返回的两个例句"},
            {"role":"user","content":f"单词为'{word}'"}
        ]
        result=self.ai_request(message)
        example_content=self.get_content(result)
        example=example_content.split("\n")[0:2]
        if len(example)==1:
            example.append("补")
            print("example缺省")
        if len(example)>2:
            example=example[:3]
            print("example获取出错")
        return example
    def get_sd_prompt(self,word):
        messages=[
            {"role":"system","content": "你熟悉Stable Diffusion的文生图工作流，能够准确的提供提示词，我想要通过Stable Diffusion生成一个单词对应的图片，你可以为我生成提示词可以用于Stable Diffusion生成这个单词的照片吗，你只需要返回提示词就可以，不需要解释其他内容"},
            {"role": "user", "content": f"比如说:{word}"},
        ]
        result=self.ai_request(messages)
        prompt=self.get_content(result)
        return prompt






if __name__ =="__main":
    pass
    # print(*["\n" for i in range(10)])
    # print(req['choices'][0]["message"]["content"])