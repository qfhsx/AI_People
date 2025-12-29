import os

# Volcano Engine Configuration
# Please replace with your actual AccessKey and SecretKey
VOLC_ACCESS_KEY = """
VOLC_SECRET_KEY = """

# Test Digital Human Resource ID
RESOURCE_ID = "250623-zhibo-linyunzhi"

# Doubao LLM Configuration
ARK_API_KEY="""
DOUBAO_MODEL_ID = "doubao-seed-1-6-251015"

# LLM Response Configuration
LLM_MAX_RESPONSE_LENGTH = 1000

# Demo Mode Configuration
DEMO_MODE = True
DEMO_VIDEO_PATH = "/Users/tal/Desktop/work/AI/ai_people/backend/temp/8731eb32-bf36-45c3-bbc4-e4f39a3d5429_avatar.mp4"
DEMO_AUDIO_PATH = "/Users/tal/Desktop/work/AI/ai_people/backend/temp/3c657e34-56b8-40a8-b1f9-c662c43d3934.mp3"
DEMO_DELAY_SECONDS = 10
DEMO_TEXT = """其实爱因斯坦并不是直接“发现”光的波粒二象性，而是通过破解光电效应的谜题，提出了光的粒子性，和之前的波动说互补，才让大家逐渐认识到光同时具有波和粒子两种性质。

当时主流都觉得光是波，像麦克斯韦的电磁理论、赫兹的实验都支持这个观点。但光电效应的现象却很矛盾：为啥光强再大，频率不够就打不出电子？为啥打出的电子动能只跟频率有关，跟强度没关系？波动说根本解释不通。

爱因斯坦受普朗克量子假说的启发——普朗克说能量是一份一份的。他大胆猜想：光本身也是由一个个能量子组成的，也就是“光子”，每个光子的能量E=hν（ν是频率，h是普朗克常数）。这样光电效应就好理解了：光子能量够大（频率够高）才能把电子从金属里打出来，频率越高能量越大，电子动能就越大；光强只是光子数量多，所以打出的电子数多，但动能不变。

后来密立根的实验证实了这个假说，大家才慢慢接受：光既有波的干涉、衍射特性，又有粒子的能量量子化特性，这就是波粒二象性啦。"""
