import re
import os
import urllib
import urllib.parse
import urllib.request
def pixiv_auto_get(pixiv_id):
    p="http://www.pixiv.net"
    path1="http://www.pixiv.net/member_illust.php?mode=medium&illust_id="+str(pixiv_id)
    path2="http://www.pixiv.net/member_illust.php?mode=manga&illust_id="+str(pixiv_id)
    request1=urllib.request.Request(path1)
    request1.add_header('Referer',p)
    request1.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request1.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')

    page = urllib.request.urlopen(request1).read()
    reg = r'src=".+?\.jpg" '
    imgre = re.compile(reg)
    imgList = re.findall(imgre, page.decode('utf-8'))
    try:
        request2=urllib.request.Request(path2)
        request2.add_header('Referer',p)
        request2.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        request2.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')

        page_m=urllib.request.urlopen(request2).read()
    except:
        print("only one pic")
        page_m=''
    multi_links=[]
    if len(re.findall('master1200.jpg',page_m))>0:
            multilist=re.findall(r'http://\S+?master1200\.jpg',page_m.decode('utf-8'))
            for link in multilist:
                if '\\' in link:
                    multilist.remove(link)
            print(multilist)
            num=0
            for target_link in multilist:
                print(target_link)
                imgName=target_link.split("/")[-1]
                referer=path1
                a=urllib.request.Request(target_link)
                a.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
                a.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7')

                a.add_header('Referer',referer)
                pic_read=urllib.request.urlopen(a)
                data=pic_read.read()
                f=open("pixiv/"+str(pixiv_id)+"_"+str(num)+".jpg","rb")
                f.write(data)
                f.close()
                link1="http://paleport.info/image-lib/"+imgName
                multi_links.append("pixiv/"+str(pixiv_id)+"_"+str(num)+".jpg")
                num+=1
            return multi_links
    else:
        x=0
        for imgurl in imgList:
            target_link=imgurl.split('"')[1]
            if target_link.endswith('master1200.jpg'):
                print(target_link)
                imgName=target_link.split("/")[-1]
                referer=path1
                a=urllib.request.Request(target_link)
                a.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
                a.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7')

                a.add_header('Referer',referer)
                pic_read=urllib.request.urlopen(a)
                data=pic_read.read()
                f=open("pixiv/"+pixiv_id+".jpg","wb")
                f.write(data)
                f.close()
                link1="http://paleport.info/image-lib/"+imgName
                return ["pixiv/"+pixiv_id+".jpg"]

if __name__=="__main__":
    pixiv_auto_get("63738701")
##http://i4.pixiv.net/c/1200x1200/img-master/img/2016/01/17/19/58/31/54765823_p1_master1200.jpg
