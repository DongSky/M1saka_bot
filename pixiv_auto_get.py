import re
import os
import urllib2
def pixiv_auto_get(pixiv_id):
    p="http://www.pixiv.net"
    path1="http://www.pixiv.net/member_illust.php?mode=medium&illust_id="+str(pixiv_id)
    path2="http://www.pixiv.net/member_illust.php?mode=manga&illust_id="+str(pixiv_id)
    request1=urllib2.Request(path1)
    request1.add_header('Referer',p)
    request1.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request1.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
    request1.add_header('Cookie','p_ab_id=7; __utmt=1; __utma=235335808.885925138.1472906278.1474957157.1479459330.5; __utmb=235335808.1.10.1479459330; __utmc=235335808; __utmz=235335808.1472906278.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=13974399=1; _ga=GA1.2.885925138.1472906278; _gat=1; PHPSESSID=19580399_24c10375b43c45f6863a16dca4bb2ace')
    page = urllib2.urlopen(request1).read()
    reg = r'src=".+?\.jpg" '
    imgre = re.compile(reg)
    imgList = re.findall(imgre, page)
    try:
        request2=urllib2.Request(path2)
        request2.add_header('Referer',p)
        request2.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        request2.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
        request2.add_header('Cookie','p_ab_id=7; __utmt=1; __utma=235335808.885925138.1472906278.1474957157.1479459330.5; __utmb=235335808.1.10.1479459330; __utmc=235335808; __utmz=235335808.1472906278.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=13974399=1; _ga=GA1.2.885925138.1472906278; _gat=1; PHPSESSID=19580399_24c10375b43c45f6863a16dca4bb2ace')
        page_m=urllib2.urlopen(request2).read()
    except:
        print("only one pic")
        page_m=''
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
                a.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
                a.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7')
                a.add_header('Cookie','p_ab_id=2; _gat=1; PHPSESSID=19580399_69940d793c80920a6974e5fa49519b8d; device_token=16b4bad8aeab37d5671f37fd686251ed; module_orders_mypage=%5B%7B%22name%22%3A%22hot_entries%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; _gat_UA-74360115-3=1; __utmt=1; __utma=235335808.1163487864.1458643928.1470694817.1470727353.22; __utmb=235335808.28.9.1470727715244; __utmc=235335808; __utmz=235335808.1470694817.21.14.utmcsr=weibo.com|utmccn=(referral)|utmcmd=referral|utmcct=/dongskycn/home; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=female=1^6=user_id=19580399=1; _ga=GA1.2.1163487864.1458643928')
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
                a.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
                a.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7')
                a.add_header('Cookie','p_ab_id=2; _gat=1; PHPSESSID=19580399_69940d793c80920a6974e5fa49519b8d; device_token=16b4bad8aeab37d5671f37fd686251ed; module_orders_mypage=%5B%7B%22name%22%3A%22hot_entries%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; _gat_UA-74360115-3=1; __utmt=1; __utma=235335808.1163487864.1458643928.1470694817.1470727353.22; __utmb=235335808.28.9.1470727715244; __utmc=235335808; __utmz=235335808.1470694817.21.14.utmcsr=weibo.com|utmccn=(referral)|utmcmd=referral|utmcct=/dongskycn/home; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=female=1^6=user_id=19580399=1; _ga=GA1.2.1163487864.1458643928')
                a.add_header('Referer',referer)
                pic_read=urllib2.urlopen(a)
                data=pic_read.read()
                f=open("/var/www/wordpress/image-lib/"+imgName,"wb")
                f.write(data)
                f.close()
                link1="http://paleport.info/image-lib/"+imgName
                return [link1]


##http://i4.pixiv.net/c/1200x1200/img-master/img/2016/01/17/19/58/31/54765823_p1_master1200.jpg
