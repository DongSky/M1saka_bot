#encoding:utf-8
import sys,json,os,urllib
import urllib.parse
import urllib.request
keys='your key'

def Tag(name):
    print("judging")
    params=urllib.parse.urlencode({
        "visualFeatures":"Categories",
        "language":"en"
    });
    url1='https://api.projectoxford.ai/vision/v1.0/analyze?%s' % params
    f=open(name,'rb');
    data1=f.read();
    req1=urllib.request.Request(url1,data=data1);
    req1.add_header('Content-Type','application/octet-stream');
    req1.add_header('Ocp-Apim-Subscription-Key',keys);
    #url1='https://api.projectoxford.ai/vision/v1.0/analyze'
    #f=open('test.jpg','rb');
    #data1=f.read();
    data=urllib.request.urlopen(req1).read();
    js_dict=json.loads(data.decode('utf-8'))
    print(js_dict["categories"])
    content=",".join([item[u'name'] for item in js_dict['categories']])
    print(content)
    return content
if __name__=="__main__":
    Tag("test_photo.jpg")
#req1=urllib2.Request(url1,data=data1);
#req1.add_header('Content-Type','application/octet-stream');

#req1.add_header('Ocp-Apim-Subscription-Key',keys);
