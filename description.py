#encoding:utf-8
import sys,json,os,urllib
import urllib.parse
import urllib.request
import time
import base64
import requests
keys = 'your key'
secret = "your secret"
def readPic(filePath):
    with open(filePath,"rb") as f:
        return f.read()
def Description(name):
    print("judging")
    url1='https://api-cn.faceplusplus.com/imagepp/beta/detectsceneandobject'
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = {}
    data['api_key'] = keys
    data['api_secret'] = secret
    data['image_base64'] = base64.b64encode(readPic(name))
    req1=requests.post(url1,data = data)
    #url1='https://api.projectoxford.ai/vision/v1.0/analyze'
    #f=open('test.jpg','rb');
    #data1=f.read();
    data=req1.content
    js_dict=json.loads(data.decode('utf-8'))
    #print(js_dict)
    content=""
    try:
        content += "scenes:\n"
        for piece in js_dict['scenes']:
            content += piece['value']+"\n"
        content += "objects:"+"\n"
        for pieve in js_dict['objects']:
            content += piece['value']+"\n"
    except:
        content = "ERROR"
    #print(content)
    return content
if __name__=="__main__":
    Description("test_photo.jpg")
#req1=urllib2.Request(url1,data=data1);
#req1.add_header('Content-Type','application/octet-stream');

#req1.add_header('Ocp-Apim-Subscription-Key',keys);
