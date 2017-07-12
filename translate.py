#!/usr/bin/env python
#coding=utf-8


"""Translation by fanyi.baidu.com online"""

import requests,hashlib,random,sys

lang_list="""
    ------language list------
    auto    自动检测
    zh    中文
    en    英语
    yue    粤语
    wyw    文言文
    jp    日语
    kor    韩语
    fra    法语
    spa    西班牙语
    th    泰语
    ara    阿拉伯语
    ru    俄语
    pt    葡萄牙语
    de    德语
    it    意大利语
    el    希腊语
    nl    荷兰语
    pl    波兰语
    bul    保加利亚语
    est    爱沙尼亚语
    dan    丹麦语
    fin    芬兰语
    cs    捷克语
    rom    罗马尼亚语
    slo    斯洛文尼亚语
    swe    瑞典语
    hu    匈牙利语
    cht    繁体中文
    vie    越南语
    """

def is_chinese(s):
    cnt=0
    for c in s:
        if c>=u'\u4e00' and c<=u'\u9fa5' : cnt+=1
    if cnt>len(s)/2:
        return True
    else:
        return False

def translate(q,fromLang = 'auto',toLang = 'zh'):

    appid = 'appid'
    secretKey = 'key'

    myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    salt = random.randint(32768, 65536)

    sign = appid+q+str(salt)+secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode('utf-8'))
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+q+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign

    try:
        r=requests.get(myurl)
        #print(eval(r.text))
        return eval(r.text)["trans_result"][0]["dst"]
    except Exception as e:
        raise
    finally:
        if r:r.close()

if __name__=="__main__":
    print(translate("月がきれい"))
