#encoding:utf-8
import sys,json,os,urllib
import urllib.parse
import urllib.request
from aip import AipOcr
APP_ID = "your id"
API_KEY = "your api key"
SECRET_KEY = "your secret"
OPTIONS = {
    "language_type":"CHN_ENG"
}
def readPic(filePath):
    with open(filePath,"rb") as f:
        return f.read()
def OCR(name):
    print("judging")
    aipocr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    data1 = readPic(name)
    result = aipocr.basicGeneral(data1,OPTIONS)
    #print(result)
    output = ""
    try:
        for piece in result["words_result"]:
            output+=piece['words']+"\n"
    except:
        output = "ERROR"
    return output
if __name__=="__main__":
    # OCR("ocrtest.png")
    print(OCR("ocr1.jpg"))
