import json,sys,urllib
import urllib.parse
import urllib.request
def shortlink(longlink):
    url1='http://apis.baidu.com/3023/shorturl/shorten?url_long='
    req = urllib.request.Request(url1+longlink)

    req.add_header("apikey", "your key")

    resp = urllib.request.urlopen(req)
    dic1=json.loads(resp.read().decode("utf-8"))
    #print(dic1['urls'][0]['url_short'])
    return dic1['urls'][0]['url_short']

if __name__=='__main__':
    print(shortlink('http://blog.csdn.net/a657941877/article/details/9063883'))
