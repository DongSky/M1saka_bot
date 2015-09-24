import re
import os
import urllib
import urllib2
def pixiv_auto_get(pixiv_id):
    path1="http://www.pixiv.net/member_illust.php?mode=medium&illust_id="+pixiv_id
    page = urllib.urlopen(path1)
    html = page.read()
    reg = r'src=".+?\.jpg" '
    imgre = re.compile(reg)
    imgList = re.findall(imgre, html)
    x=0
    for imgurl in imgList:
        target_link=imgurl.split('"')[1]
        if target_link.endswith('master1200.jpg'):
            print(target_link)
            imgName=target_link.split("/")[-1]
            referer=path1
            a=urllib2.Request(target_link)
            a.add_header('Referer',referer)
            pic_read=urllib2.urlopen(a)
            data=pic_read.read()
            f=open("/var/www/wordpress/image-lib/"+imgName,"wb")
            f.write(data)
            f.close()
            link1="http://paleport.cf/image-lib/"+imgName
            return link1
