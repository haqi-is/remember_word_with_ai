<<<<<<< HEAD
# remember_word_with_ai
通过sd和大语言模型背单词
=======
测试使用环境
python3.7
通义千问qwen-plus（适配了OpenAI Python SDK的大语言模型大概率能使用）

一、安装环境
切换至项目根目录
pip install -r requirement.txt

二、配置
配置文本大模型信息（测试使用的是qwen-plus）
在config_user.py文件中，配置"api_key"、"model"、"base_url"信息（这些信息需要从模型官网申请，未配置会导致报错）

三、开始运行
切换到项目根目录
python main.py

四、可选修改
Stable Diffusion
默认单词的图像生成功能是关闭的，如需开启sd图像生成请在config_system.json中"sd_is_work"设置为true（默认为false），(重点!)同时需要本地的sd开启且能正常使用，即可直接调用到sd。

如果你的sd修改了默认端口，则请在sdOBJ中的将self.url配置成您的端口




五、注意事项
1.生成的图像保存在项目的images文件夹中
2.如果需要切换Stable Diffusion模型和图像属性（保持默认也可以正常使用），请移步到sdOBJ.py中的sdOBJ对象中的set_model、txt_to_img_post方法中修改
>>>>>>> 1eff9d8 (初版)
