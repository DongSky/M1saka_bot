#encoding:utf-8
#利用urllib2模块获取搜索内容前十名的磁链
import re
import os
import urllib
import urllib2
def btdiggtop10get(link):
    referer_link="http://btdigg.org"
#    list_symbol=r'<tr><td class=.+?\.title="Download via magnet-link '
    symbol=r'magnet:.+? '
    titlesymbol=r'>.+?</a></td></tr></table>'
#    symbol0=re.compile(list_symbol)
    symbol1=re.compile(symbol)
    symbol2=re.compile(titlesymbol)
    a=urllib2.Request(link)
    a.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    a.add_header('Referer',referer_link)
    a.add_header("User-Agent", 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12')
    print('pass')
    b=urllib2.urlopen(a).read()
    print('read')
    #print(b)
    #contentlist=re.findall(symbol0,b)
    magnetlist=re.findall(symbol1,b)
    print(magnetlist)
    #print(magnetlist)
    i=0
    while i<len(magnetlist):
        magnetlist[i]=magnetlist[i].split('"')[0]
        #print(magnetlist[i])
        i=i+1
    titlelist=re.findall(symbol2,b)
    print(titlelist)
    i=0
    while i<len(titlelist):
        titlelist[i]=titlelist[i].split('</a></td></tr></table>')[-2]
        titlelist[i]=titlelist[i].split('>')[-1]
        i=i+1
    #magnetlist.extend(findmagnet)
    #titlelist.extend(findtitle)
    outputlist=[]
    for title in titlelist:
        if title.startswith('Files') or title.startswith('Next \xe2\x86\x92'):
            titlelist.remove(title)
    print(titlelist)
    print(len(titlelist))
    try:
        i=0
        while i<10 and i<len(magnetlist):
            outputlist.append(titlelist[i]+'\n'+magnetlist[i])
            i+=1
        return outputlist
    except:
        i=2
        while i<len(titlelist):
            outputlist.append(titlelist[i]+'\n'+magnetlist[i])
            i+=1
        return outputlist
#    while i<10:
#        outputlist.append(titlelist[i]+'\n'+magnetlist[i])
#        i=i+1
    #print(outputlist)
#return outputlist
