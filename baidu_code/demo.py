# coding:utf-8
#谷雨课堂第11期，做一个完整的语音助理
#知识点：语音识别
#https://github.com/cn09876/guyuedu/blob/master/%E3%80%90%E8%B0%B7%E9%9B%A8%E8%AF%BE%E5%A0%82%E3%80%91%E6%95%B0%E5%AD%A6%E4%B8%8EPython/No.11%20%E5%81%9A%E4%B8%80%E4%B8%AA%E8%AF%AD%E9%9F%B3%E5%8A%A9%E6%89%8B/py_asr.py

import time
import wave
import pyaudio
from aip import AipSpeech
import win32com.client
import pygame

#播放音乐
def play_music():
    pygame.mixer.init()
    track = pygame.mixer.music.load('./seeyouagain.mp3')
    pygame.mixer.music.play()
    time.sleep(13)
    pygame.mixer.music.stop()

#输出当前日期和时间
def now_():
    return time.strftime('现在是: %Y年%m月%d日%H点%M分',time.localtime(time.time()))
    
#语音合成输出
def speak(s):
    print("-->"+s)
    win32com.client.Dispatch("SAPI.SpVoice").Speak(s)

#调用百度云，进行语音识别
def audio_discern(audio_path = "./test.wav",audio_type = "wav"):

    """ 百度云的ID，免费注册 """
    APP_ID = '22895018' 
    API_KEY = 'zzxWTnPxgKxfv4jMcGij1xFH' 
    SECRET_KEY = '1uh14bAwqWvM6aaKxwvawnMdbe9RIScQ'
 
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # 读取文件
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    # 识别本地文件
    text = client.asr(get_file_content(audio_path), audio_type, 16000)
    return text

#用Pyaudio库录制音频
def audio_record(out_file, rec_time):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16 #16bit编码格式
    CHANNELS = 1 #单声道
    RATE = 16000 #16000采样频率
    p = pyaudio.PyAudio()
    # 创建音频流
    stream = p.open(format=FORMAT, # 音频流wav格式
                    channels=CHANNELS, # 单声道
                    rate=RATE, # 采样率16000
                    input=True,
                    frames_per_buffer=CHUNK)
    print("Start Recording...")
    frames = [] # 录制的音频流
    # 录制音频数据
    for i in range(0, int(RATE / CHUNK * rec_time)):
        data = stream.read(CHUNK)
        frames.append(data)
    # 录制完成
    #print(frames)
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # 保存音频文件
    with wave.open(out_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    


while(True):
    print("请讲话...")

    audio_path = "./test1.wav"
    # 录制语音指令
    audio_record(audio_path, 3) 

    print("开始做语音识别...")
    ret =  audio_discern(audio_path) # 识别语音指令    
    if ret["err_no"] == 0:
        text = ret["result"][0]      
        print(text)

        if '小娜' in text:
            speak('我在的')

        elif '诗' in text:
            speak('白日依山尽，黄河入海流。 欲穷千里目，更上一层楼。')

        elif '订' in text:
            speak('你的余额不足')

        elif '天气' in text:
            speak('今天天气风和日丽的，一起出去玩啊')

        elif '人工智能' in text:
            speak('我就是人工智能，哈哈哈')

        elif '猫' in text:
            speak('喵喵喵喵喵')

        elif '上学' in text:
            speak('当然在谷雨课堂了，微信搜索华纳网就能看到所有教程了.')

        elif '狗' in text:
            speak('旺旺旺旺旺')

        elif '几点' in text:
            speak(now_())

        elif '名字' in text:
            speak('我叫晓娜')

        elif '播放' in text:
            play_music()

        # 如果是"退出"指令则结束程序
        elif text.find("退") != -1: 
            speak('臣妾退下了')
            break
        else:
            speak('我没有理解你说的话')

        # 延时一小会儿
        time.sleep(0.5) 
    else:
        print('错误：'+ret)
