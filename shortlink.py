import json,sys,urllib2
def shortlink(longlink):
    url1='http://apis.baidu.com/3023/shorturl/shorten?url_long='
    req = urllib2.Request(url1+longlink)

    req.add_header("apikey", "83a0fc03038060891b12cdcc7bd8d695")

    resp = urllib2.urlopen(req)
    dic1=json.loads(resp.read())
    print(dic1['urls'][0]['url_short'])
    return dic1['urls'][0]['url_short']