#encoding:utf-8
import sys,json,urllib
import urllib.parse
import urllib.request
# def weatherinfo(cityname):
#     url1='http://apis.baidu.com/apistore/weatherservice/cityname?cityname='
#     request1=urllib2.Request(url1+cityname)
#     request1.add_header("apikey","83a0fc03038060891b12cdcc7bd8d695")
#     response1=urllib2.urlopen(request1)
#     dic1=json.loads(response1.read())
#     print(dic1)
#     info=cityname+'\n'
#     info=info+'weather:'+dic1['retData']['weather']+'\n'+'temprature:'+dic1['retData']['temp'];
#     print(info)
#     return info

def weatherinfo(cityname):
    params=urllib.parse.urlencode({
        'key':'your key',
        'language':'zh-Hans',
        'location':cityname,
        'unit':'c',
        'start':'0',
        'end':'3'
    })
    url1='https://api.seniverse.com/v3/weather/daily.json?%s'%params
    request1=urllib.request.Request(url1)
    data=urllib.request.urlopen(request1).read()
    js_dict=json.loads(data.decode('utf-8'))
    print(js_dict)
    content=''
    for item in js_dict['results'][0]['daily']:
        str1=item['date']+":day "+item['text_day']+", night "+item['text_night']+", "+item['high']+'/'+item['low']+' degree(C)\n'
        content+=str1
    print(content)
    return content

if __name__=="__main__":
    weatherinfo('哈尔滨')
