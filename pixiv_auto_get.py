import re
import os
import urllib
import urllib2
def pixiv_auto_get(pixiv_id):
    path1="http://www.pixiv.net/member_illust.php?mode=medium&illust_id="+pixiv_id
    path2="http://www.pixiv.net/member_illust.php?mode=manga&illust_id="+pixiv_id
    page = urllib.urlopen(path1)
    html = page.read()
    reg = r'src=".+?\.jpg" '
    imgre = re.compile(reg)
    imgList = re.findall(imgre, html)
    page_m=urllib.urlopen(path2).read()
    multi_links=[]
    if len(re.findall('master1200.jpg',page_m))>0:
            multilist=re.findall(r'http://\S+?master1200\.jpg',page_m)
            for link in multilist:
                if '\\' in link:
                    multilist.remove(link)
            print(multilist)
            for target_link in multilist:
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
                link1="http://paleport.info/image-lib/"+imgName
                multi_links.append(link1)
            return multi_links
    else:
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
                link1="http://paleport.info/image-lib/"+imgName
                return [link1]


##http://i4.pixiv.net/c/1200x1200/img-master/img/2016/01/17/19/58/31/54765823_p1_master1200.jpg
