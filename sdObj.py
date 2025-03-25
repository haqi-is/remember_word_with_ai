import io
import os
import base64
from PIL import Image
import requests
from config_user import config
import time
from AiObj import AiObj
class sdObj():
    def __init__(self):
        self.url="http://127.0.0.1:7860"
        self.root_images_path=config["root_image_path"]
        self.ai=AiObj(
            config["api_key"],
            config["model"],
            config["base_url"]
        )
    def check_sd_enable(self):
        check_enable_tag=True
        try:
            self.set_model()
        except:
            check_enable_tag=False
            return check_enable_tag
        else:
            return check_enable_tag

    def set_model(self):
        # 设置切换模型
        option_payload = {
            "sd_model_checkpoint": "helloobjects_V15evae.safetensors [6d82a674e1]",
            "CLIP_stop_at_last_layers": 2
        }

        response = requests.post(url=f'{self.url}/sdapi/v1/options', json=option_payload)
    def txt_to_img_post(self,word,prompt):
        payload = {
            "prompt": prompt,
            "steps": 28,
            "width": 512,
            "height": 512,
            "sampler_index": "DPM++ 2M Karras",
        }

        response = requests.post(url=f'{self.url}/sdapi/v1/txt2img', json=payload)

        r = response.json()
        image=None
        for i in r['images']:
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
            image_path=os.path.join(config['root_image_path'],f'{word}.png')
            image.save(image_path)
        print("完成")
        return image_path
    def show_image(self,image_path):
        import cv2

        # 读取图片
        image = cv2.imread(image_path)

        # 显示图片
        cv2.imshow("Image", image)

        # 等待用户关闭窗口
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def find_image(self,word):
        file_list=os.listdir(self.root_images_path)
        for i in file_list:
            if os.path.isfile(os.path.join(self.root_images_path,i))!=True:
                file_list.remove(i)
        for i in file_list:
            filename=i.split(".")[0]
            if filename==word:
                return os.path.join(self.root_images_path,i)
        else:
            return False
    def txt_to_img(self,word):
        image_path=self.find_image(word)
        if image_path:
            self.show_image(image_path)
        else:
            print(f"为您生成{word}照片中...")
            if self.check_sd_enable():
                print(f"为{word}生成提示词中...")
                prompt=self.ai.get_sd_prompt(word)
                self.set_model()
                print(f"prompt:  {prompt}")
                print(f"已将{word}的prompt提交给Stable Diffusion")
                print(f"为{word}生成图片中...")
                image_path=self.txt_to_img_post(word,prompt)
                self.show_image(image_path)
            else:
                print("生图引擎未启动!")
                time.sleep(2)



