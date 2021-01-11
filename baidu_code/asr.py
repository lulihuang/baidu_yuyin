#coding:utf-8
#https://blog.csdn.net/sinat_35162460/article/details/86544772
# 百度云语音识别Demo，实现对本地语音文件的识别。
# 需安装好python-SDK，录音文件不不超过60s，文件类型为wav格式。
# 音频参数需设置为 单通道 采样频率为16K PCM格式 可以先采用官方音频进行测试

# 导入AipSpeech  AipSpeech是语音识别的Python SDK客户端
from aip import AipSpeech
import os

''' 你的APPID AK SK  参数在申请的百度云语音服务的控制台查看'''
APP_ID = '22895018'
API_KEY = 'zzxWTnPxgKxfv4jMcGij1xFH'
SECRET_KEY = '1uh14bAwqWvM6aaKxwvawnMdbe9RIScQ'

# 新建一个AipSpeech
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 读取文件
def get_file_content(filePath):   #filePath  待读取文件名
	with open(filePath, 'rb') as fp:
		return fp.read()

# 识别本地文件
text=client.asr(get_file_content('./test/009.amr'), 'amr', 16000, {'dev_pid': 1537,})
result_text=text['result'][0]
print(result_text)

