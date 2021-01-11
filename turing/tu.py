
# coding:utf-8
import requests
import json
import base64
import wave
from pydub import AudioSegment ###需要安装pydub、ffmpeg
import io
import os
import serial
import RPi.GPIO as GPIO
import urllib2
import urllib
import time
import datetime
import re
import hashlib
import struct
import sys
 
 
#ser = serial.Serial("/dev/rfcomm0",9600)
baidu_server = "https://openapi.baidu.com/oauth/2.0/token?"
grant_type = "client_credentials"
client_id = "WUPlWzkwF5KbG1typ8EOGglh"
client_secret = "ZAs8igGeEOF2plKP9kGmIXgXKeeXdoGN" #填写Secret Key
 
#合成请求token的URL
url = baidu_server+"grant_type="+grant_type+"&client_id="+client_id+"&client_secret="+client_secret
 
#获取token
res = urllib2.urlopen(url).read()
data = json.loads(res)
token = data["access_token"]
#print token
 
GPIO_PIN = 24
GPIO.setmode(GPIO.BCM)
#GPIO.setup(GPIO_PIN, GPIO.IN)
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
 
 
class BaiduRest:
    def __init__(self, cu_id, api_key, api_secert):
        # token认证的url
        self.token_url = "https://openapi.baidu.com/oauth/2.0/token"
        # 语音合成的resturl
        self.getvoice_url = "http://tsn.baidu.com/text2audio"
        # 语音识别的resturl
        self.upvoice_url = 'http://vop.baidu.com/server_api'
        self.cu_id = cu_id
        self.getToken(api_key, api_secert)
        return
 
    def getToken(self, api_key, api_secert):
        # 1.获取token
        data={'grant_type':'client_credentials','client_id':api_key,'client_secret':api_secert}
        r=requests.post(self.token_url,data=data)
        Token=json.loads(r.text)
        self.token_str = Token['access_token']
 
 
    def getVoice(self, text, filename):     #语音合成
        # 2. 向Rest接口提交数据
        data={'tex':text,'lan':'zh','cuid':self.cu_id,'ctp':1,'tok':self.token_str}
        #data={'tex':text,'lan':'en','cuid':self.cu_id,'ctp':1,'tok':self.token_str}
        r=requests.post(self.getvoice_url,data=data,stream=True)
        voice_fp = open(filename,'wb')
        voice_fp.write(r.raw.read())
        # for chunk in r.iter_content(chunk_size=1024):
            # voice_fp.write(chunk)
        voice_fp.close()
 
    def ConvertToWav(self,filename,wavfilename):       #wav 转 mp3
        #先从本地获取mp3的bytestring作为数据样本
        fp=open("out.mp3",'rb')
        data=fp.read()
        fp.close()
        #主要部分
        aud=io.BytesIO(data)
        sound=AudioSegment.from_file(aud,format='mp3')
        raw_data = sound._data
        #写入到文件，验证结果是否正确。
        l=len(raw_data)
        f=wave.open(wavfilename,'wb')
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(16000)
        f.setnframes(l)
        f.writeframes(raw_data)
        f.close()
        return wavfilename
 
while 1:
    print ('等待触发：')
    if(GPIO.input(GPIO_PIN) == 1):
 
        print ('正在录音')
        os.system('arecord -d 4 -r 8000 -c 1 -t wav -f S16_LE -D plughw:1,0  ddd.wav')
        #设置音频属性，根据百度的要求，采样率必须为8000，压缩格式支持pcm（不压缩）、wav、opus、speex、amr
        VOICE_RATE = 8000
        WAVE_FILE = "ddd.wav" #音频文件的路径
        USER_ID = "zhp-fw" #用于标识的ID，可以随意设置
        WAVE_TYPE = "wav"
        print ('录音结束,正在识别')
 
        #打开音频文件，并进行编码
        f = open(WAVE_FILE, "r")
        speech = base64.b64encode(f.read())
        size = os.path.getsize(WAVE_FILE)
        update = json.dumps({"format":WAVE_TYPE, "rate":VOICE_RATE, 'channel':1,'cuid':USER_ID,'token':token,'speech':speech,'len':size})
        headers = { 'Content-Type' : 'application/json' } 
        url = "http://vop.baidu.com/server_api"
        req = urllib2.Request(url, update, headers)
 
        r = urllib2.urlopen(req)
 
        #语音识别
        t = r.read()
        result = json.loads(t)
        #print result
        if result['err_msg']=='success.':
            word = result['result'][0].encode('utf-8')
            #word = result['result'].encode('utf-8')
            if word!='':
                #if word[len(word)-3:len(word)]==',':
                    #print word[0:len(word)-3]
                #else:
                #串口发送
                t1 = word
                t2 = t1.decode("utf-8")  #转换成 unicode 编码
                #print(t2,type(t2))
                t3 = t2.encode("gbk")   #解码成 gbk 中文
                #print(t3,type(t3))
                t4 = t1[:-1]
                t5 = t4[:-1]
                t6 = t3[:-1]
                t7 = t6[:-1]
                #s = ser.write(t7)
                #s8 = ser.write('\r\n')
                #ser.close()
                print (t5)   
            else:
                print ("音频文件不存在或格式错误")
        else:
            print ("错误")
            
        #串口发送
        '''
        t1 = word
        t2 = t1.decode("utf-8")  #转换成 unicode 编码
        #print(t2,type(t2))
        t3 = t2.encode("gbk")   #解码成 gbk 中文
        #print(t3,type(t3))
        t4 = t1[:-1]
        t5 = t4[:-1]
        s = ser.write(t5)
        s = ser.write('\r\n')
        #ser.close()
        '''
        #s = ser.write("word sys")    
        #s = ser.write('\r\n')
        #图灵
        print('稍等，正在回答你的问题：')
        time.sleep(1)
        '''
        def getHtml(url):  
            page = urllib.urlopen(url)  
            html = page.read()  
            return html
        key = '4e348190e92547fe85efc3fb137345e7'  
        api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='  
        #        info = raw_input('我: ')  
        request = api + word  
        response = getHtml(request)  
        dic_json = json.loads(response)  
        print '答: '.decode('utf-8') + dic_json['text']
        '''
        reload(sys) 
        sys.setdefaultencoding('utf-8') 
 
        API_KEY_tuling = '4e348190e92547fe85efc3fb137345e7'
        raw_TULINURL = "http://www.tuling123.com/openapi/api?key=%s&info=" % API_KEY_tuling
 
        def result():
            for i in range(1,100):
                #queryStr = raw_input("我:".decode('utf-8'))
                queryStr = word
                
                TULINURL = "%s%s" % (raw_TULINURL,urllib2.quote(queryStr))
                req = urllib2.Request(url=TULINURL)
                result = urllib2.urlopen(req).read()
                hjson=json.loads(result)
                length=len(hjson.keys())
                content=hjson['text']
 
                if length==3: 
                    #return 'robots:' +content+hjson['url']
                    return  content+hjson['url']
                elif length==2:           
                    #return 'robots:' +content
                    return content
 
        #print "你好，请输入内容:".decode('utf-8')
        contents=result()
        
        print (contents)
        #百度语音合成
        api_key = "WUPlWzkwF5KbG1typ8EOGglh" 
        api_secert = "ZAs8igGeEOF2plKP9kGmIXgXKeeXdoGN"
        # 初始化
        bdr = BaiduRest("test_python", api_key, api_secert)
        # 将字符串语音合成并保存为out.mp3
        #bdr.getVoice("student", "out.mp3")
        bdr.getVoice(contents, "out.mp3")
        # 识别test.wav语音内容并显示
        #print(bdr.getText(bdr.ConvertToWav("out.mp3","test.wav")))
        os.system('mplayer out.mp3')  
 
