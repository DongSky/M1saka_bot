import re
import os
import urllib
import urllib2
def btdiggtop10get(link):
    referer_link="http://btdigg.org"
    symbol=r'magnet:.+? '
    symbol1=re.compile(symbol)
    a=urllib2.Request(link)
    a.add_header('Accept', 'Accept	text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    a.add_header('Referer',referer_link)
    a.add_header("User-Agent", 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12')
    b=urllib2.urlopen(a).read()
    magnetlist=re.findall(symbol1,b)
    for link in magnetlist:
        link=link.split('"')[1]
        print(link)
    return magnetlist
