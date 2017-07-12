#encoding:utf-8
import urllib.parse
import urllib.request
import requests,json,os,sys,urllib

key="your key"


def search(query):
    params=urllib.parse.urlencode({
        'q':query
    })
    url1='https://api.cognitive.microsoft.com/bing/v5.0/search?%s'%params
    request1=urllib.request.Request(url1)
    request1.add_header('Ocp-Apim-Subscription-Key',key);
    data=urllib.request.urlopen(request1).read().decode('utf-8')
    js_dict=json.loads(data)
    #print(js_dict)
    if not 'error' in js_dict.keys():
        webpage=js_dict['webPages']
        #image=js_dict['images']
        contentstr="Search Result:\n"
        for item in webpage['value']:
            contentstr+=item['name']+'\n'+item['url']+'\n'
    else:
        contentstr="search failed"
    return contentstr
if __name__=="__main__":
    print(search("Visual Studio"))
