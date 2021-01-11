#coding:utf-8
#https://ai.baidu.com/ai-doc/SPEECH/7k38lxpwf
# 百度云语音合成Demo，实现对本地文本的语音合成。
# 需安装好python-SDK，待合成文本不超过1024个字节
# 合成成功返回audio.mp3 否则返回错误代码

# 导入AipSpeech  AipSpeech是语音识别的Python SDK客户端
from aip import AipSpeech
import os

''' 你的APPID AK SK  参数在申请的百度云语音服务的控制台查看'''
APP_ID = '22895018'
API_KEY = 'zzxWTnPxgKxfv4jMcGij1xFH'
SECRET_KEY = '1uh14bAwqWvM6aaKxwvawnMdbe9RIScQ'
# 新建一个AipSpeech
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

'''
#1、单句
result  = client.synthesis('你好,小氢', 'zh', 1, {'vol': 5,})
# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
   with open('output.mp3', 'wb') as f:
        f.write(result)
		
'''
#2、多句
# 将本地文件进行语音合成
def tts(filename):
    f = open(filename,'r')
    command = f.read()
    if len(command) != 0:
        word = command
    f.close()
    result  = client.synthesis(word,'zh',1, {
        'vol': 5,'per':0,
    })
	
# 合成正确返回audio.mp3，错误则返回dict 
    if not isinstance(result, dict):
        with open('audio.mp3', 'wb') as f:
            f.write(result)
        f.close()
        print ('tts successful')

# main

if __name__ == '__main__':

    tts('demo.txt')

