#encoding:utf-8
#利用urllib2模块获取搜索内容前十名的磁链
import re
import os
import urllib
#import urllib.parse
#import urllib.request
import requests
# from poster.encode import multipart_encode
# from poster.streaminghttp import register_openers

def btdiggtop10get(link):
    print(link)
    #register_openers()
    #datagen,headers=multipart_encode({"keyword":link})
    #referer_link="http://btdigg.co/"
#    list_symbol=r'<tr><td class=.+?\.title="Download via magnet-link '
    symbol=r"magnet:.+?'"
    titlesymbol=r'target="_blank">.+?</a>'
#    symbol0=re.compile(list_symbol)
    symbol1=re.compile(symbol)
    symbol2=re.compile(titlesymbol)
    #a=urllib.request.Request(link)
    headers={}
    headers["Accept"]="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    headers["Connection"]="keep-alive"
    headers["Referer"]="http://btdigg.xyz/"
    headers["User-Agent"]="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    #print(headers)
    request1=requests.post("http://btdigg.xyz/",data={"keyword":link},headers=headers)
    str1=request1.content
    #print(b)
    #contentlist=re.findall(symbol0,b)
    maglnk=re.findall("magnet:?.+?'", str1.decode('utf-8'))
    for i in range(len(maglnk)):
        maglnk[i]=maglnk[i].split("'")[0]
    print(maglnk)
    print(len(maglnk))
    #print(magnetlist)
    # i=0
    # while i<len(magnetlist):
    #     magnetlist[i]=magnetlist[i].split('"')[0]
    #     #print(magnetlist[i])
    #     i=i+1
    titlelist_=re.findall(symbol2,str1.decode('utf-8'))
    print(titlelist_)
    print(len(titlelist_))
    titlelist=[]
    temp=[]
    for i in titlelist_:
        if i.startswith('target="_blank"><img'):
            pass
        else:
            temp.append(i)
    for i in range(len(temp)):
        titlelist.append(re.sub(".+?</script>","","".join("".join("".join(temp[i].split('target="_blank">')[1].split("<b>")).split("</b>")).split("</a>"))))
        #titlelist[i]=titlelist[i].split('</a>')[-0].split("</b>")[1]
    #magnetlist.extend(findmagnet)
    #titlelist.extend(findtitle)
    outputlist=[]
    # for title in titlelist:
    #     if title.startswith('Files') or title.startswith('Next \xe2\x86\x92'):
    #         titlelist.remove(title)
    for i in titlelist:
        print(i)
    print(len(titlelist))
    try:
        i=0
        while i<len(maglnk):
            outputlist.append(titlelist[i]+'\n'+maglnk[i])
            i+=1
        return outputlist
    except:
        i=2
        while i<len(titlelist):
            outputlist.append(titlelist[i]+'\n'+maglnk[i])
            i+=1
        return outputlist
if __name__=="__main__":
    btdiggtop10get("ABP-521")
#    while i<10:
#        outputlist.append(titlelist[i]+'\n'+magnetlist[i])
#        i=i+1
    #print(outputlist)
#return outputlist
