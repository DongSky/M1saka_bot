#encoding:utf-8
import urllib2
import os
import sys
import json
import thread
import telegram
import pixiv_auto_get
import btdiggTop10
import command_line
import randimg
import weatherinfo
import shortlink

#global bot
global last_update_id
reload(sys)
sys.setdefaultencoding("utf-8")
def pixiv_get(bot,pixiv_id):
    aaaa=pixiv_auto_get.pixiv_auto_get(pixiv_id)
    try:
        for aaa in aaaa:
            try:
                bot.sendPhoto(chat_id=chatid,photo=aaa)
            except:
                bot.sendMessage(chat_id=chatid,text=aaa)
    except:
        bot.sendMessage(chat_id=chatid,text="error......")
    del aaaa
def short_link(bot,long_link):
    short=shortlink.shortlink(long_link)
    bot.sendMessage(chat_id=chatid,text=short)
    del short

def weather_info(bot,cityname):
    info=weatherinfo.weatherinfo(cityname)
    bot.sendMessage(chat_id=chatid,text=info)
    del info

bot=telegram.Bot('yours:yours')
try:
    last_update_id=bot.getUpdates()[-1].update_id
except IndexError:
    last_update_id=None
while True:
    updates=bot.getUpdates(offset=last_update_id)
    for update in updates:
        chatid=update.message.chat_id
        content=update.message.text
        if content.startswith('/cmd') and '$' in content:
            chatname=update['message']['from_user']['username']
            command_pre=content.split('$')[1]
            k=command_line.commandline(chatname,command_pre)
            bot.sendMessage(chat_id=chatid,text=k)
        if content=="/test":
            bot.sendMessage(chat_id=chatid,text="testing")
        elif content=="/randimg":
            bot.sendPhoto(chat_id=chatid,photo=randimg.randimg())
        elif content=="/about":
            bot.sendMessage(chatid,"a virtual girlfriend demo(testing)")
        elif content.startswith("/pixiv")and '#' in content:
            if content=='/pixiv' or content.split('#')[1]=='':
                bot.sendMessage(chat_id=chatid,text='请按照格式"/pixiv#content"发送')
            else:
                pixiv_id=content.split('#')[1]
                thread.start_new_thread(pixiv_get,(bot,pixiv_id))

        elif content=="/about_moebean":
            aboutcontent="某初学者为了装装逼加学习Python，\n基于github上的Python-telegram-bot项目开发的简易机器人，\n如果后期成功脱团并且有了思路会继续改进为真正的虚拟女友项目。\n具体功能如下：\n/about--获取帮助\n/pixiv#p站图片ID--自动获取图片（暂时只能实现第一张获取且需要本人服务器中转\n/google$内容或者/baidu$内容--搜索相关内容\n/top10btdigg$search_content：搜索btdigg某特定内容排行前十的磁力链接\n未完待续\n欢迎关注微博@DongSky苍白文\n或者Twitter@DongSkyCN"
            bot.sendMessage(chat_id=chatid,text=aboutcontent)
        elif content.startswith('/google')and '$'in content:
            if content=='/google':
                bot.sendMessage(chat_id=chatid,text='请按照格式"/google$content"发送')
            else:
                search_content=content.split('$')[1]
                if search_content=='':
                    bot.sendMessage(chat_id=chatid,text='请按照格式"/google$content"发送')
                else:
                    link='https://www.google.com/?gfe_rd=cr&ei=5zzlVYSoFueN8QeOjKuoDQ&gws_rd=cr&fg=1#q='+search_content
                    bot.sendMessage(chat_id=chatid,text=link)
                    del link
        elif content.startswith("/baidu")and '$'in content:
            search_content=content.split("$")[1]
            link="https://www.baidu.com/from=844b/s?word="+search_content
            bot.sendMessage(chat_id=chatid,text=link)
            del link
        elif content.startswith('/weather')and '$'in content:
            try:
                cityname=content.split('$')[1]
                thread.start_new_thread(weather_info,(bot,cityname))
            except:
                bot.sendMessage(chat_id=chatid,text='error......')
        elif content.startswith('/short')and ' 'in content:
            try:
                long_link=content.split(' ')[1]
                thread.start_new_thread(short_link,(bot,long_link))
            except:
                bot.sendMessage(chat_id=chatid,text='error......')

        elif content.startswith('/btdigg')and '$'in content:
            if content=='btdigg' or content.split('$')[1]=='':
                bot.sendMessage(chat_id=chatid,text='请按照格式"/btdigg$content"发送')
            else:
                search_content=content.split('$')[1]
                try:
                    list1=btdiggTop10.btdiggtop10get(search_content)
                    print(list1)
                    output=""
                    i=0
                    while i<len(list1):
                        output+=list1[i]+'\n'
                        print(output)
                        i+=1
                    #output=list1[0]+'\n'+list1[1]+'\n'+list1[2]+'\n'+list1[3]+'\n'+list1[4]+'\n'+list1[5]+'\n'+list1[6]+'\n'+list1[7]+'\n'+list1[8]+'\n'+list1[9]
                    bot.sendMessage(chat_id=chatid,text=output)
                except:
                    output="error:something wrong"
                    bot.sendMessage(chat_id=chatid,text=output)
        else:
	        pass
        last_update_id=updates[-1].update_id+1
