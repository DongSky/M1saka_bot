#encoding:utf-8
import sys,urllib2,json
def weatherinfo(cityname):
    url1='http://apis.baidu.com/apistore/weatherservice/cityname?cityname='
    request1=urllib2.Request(url1+cityname)
    request1.add_header("apikey","your key")
    response1=urllib2.urlopen(request1)
    print(type(response1))
    dic1=json.loads(response1.read())

    print(dic1['retData'])
    info=cityname+'\n'
    info=info+'weather:'+dic1['retData']['weather']+'\n'+'temprature'+dic1['retData']['temp'];
    return info
