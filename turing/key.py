#coding:utf-8
import time
import os
import pygame
import urllib.request
import json
from aip import AipSpeech
import speech_recognition as sr
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)#忽略百度api连接时的报错信息。

# Baidu Speech API
APP_ID = '22895018'
API_KEY = 'zzxWTnPxgKxfv4jMcGij1xFH'
SECRET_KEY = '1uh14bAwqWvM6aaKxwvawnMdbe9RIScQ'

client = AipSpeech(APP_ID,API_KEY,SECRET_KEY)

#Turing API
TURING_KEY = "cafb7e6da9d64e6292434b569aa9b26b"
API_URL = "http://openapi.tuling123.com/openapi/api/v2"

# 录音
def rec(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("please say something")
        audio = r.listen(source)

    with open("recording.wav", "wb") as f:
        f.write(audio.get_wav_data())

# 百度语音转文字
def listen():
    with open('recording.wav', 'rb') as f:
        audio_data = f.read()

    result = client.asr(audio_data, 'wav', 16000, {
        'dev_pid': 1536,
    })

    text_input = result["result"][0]

    print("我说: " + text_input)
    Robot_think(text_input)


# 图灵处理
def Robot_think(text_input):
    req = {
    "perception":
    {
        "inputText":
        {
            "text": text_input
        },

        "selfInfo":
        {
            "location":
            {
                "city": "福州",
                "province": "福建",
                "street": "智恒路"
            }
        }
    },
    "userInfo":
    {
        "apiKey": TURING_KEY,
        "userId":  "starky"  #"这里随便填"
    }
}
    # print(req)
    # 将字典格式的req编码为utf8
    req = json.dumps(req).encode('utf8')
    # print(req)

    http_post = urllib.request.Request(API_URL, data=req, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(http_post)
    response_str = response.read().decode('utf8')
    # print(response_str)
    response_dic = json.loads(response_str)
    # print(response_dic)

    intent_code = response_dic['intent']['code']
    results_text = response_dic['results'][0]['values']['text']
    print("AI说: " + results_text)
    du_say(results_text)
    play_mp3('robot.mp3')
# 文字转语音
def du_say(results_text):
    # per 3是汉子 4是妹子，spd 是语速，vol 是音量
    result = client.synthesis(results_text, 'zh', 1, {
        'vol': 5, 'per': 4, 'spd': 4
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('robot.mp3', 'wb') as f:
            f.write(result)

# 播放Mp3文件
def play_mp3(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    
    

if __name__ == '__main__':
    while True:
        rec()
        listen()
        
        
        
        
        
