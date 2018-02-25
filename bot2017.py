#encoding:utf-8
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,ConversationHandler)
import logging,os,urllib,json
import pixiv_auto_get
import description
#import tag
import ocr
import mail
import shortlink
import weatherinfo
import btdiggTop10
import translate
import qna
from status_code import *
import netease_music_lib
import NHentai
#import bingsearch
#initialize logging module

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",level=logging.INFO)
logger=logging.getLogger(__name__)

#    some modules
def start(bot, update):
    update.message.reply_text('Hi!')
def echo_request(bot, update):
    update.message.reply_text('hello world')

def photo(bot, update):
    print("photo in")
    user=update.message.from_user
    photo_file=bot.get_file(update.message.photo[-1].file_id)
    photo_file.download("test_photo.jpg")
    logger.info("Photo of %s: %s" % (user.first_name, 'test_photo.jpg'))
    update.message.reply_text("get")
    update.message.reply_photo(open("test_photo.jpg","rb"))
    return 1

def btdigg_start(bot, update):
    update.message.reply_text("input the content")
    return 1
def btdigg_get(bot,update):
    print("btdigg_get in")
    content=str(update.message.text)
    print(content)
    outputlist=btdiggTop10.btdiggtop10get(content)
    reply_str=""
    if len(outputlist)==0:
        reply_str+="error, no resources"
    else:
        cnt_=0
        for out in outputlist:
            reply_str+=out+"\n"
            cnt_+=1
            if cnt_>=min(10,len(outputlist)):
                break
    update.message.reply_text(reply_str)
    return ConversationHandler.END

def pixivget(bot, update):
    update.message
    pic_get=pixiv_auto_get.pixiv_auto_get(pixiv_id=update.message.text.split("$")[1])
    for pic_pos in pic_get:
        update.message.reply_photo(open(pic_pos,"rb"))
    return 1
def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Cancel',reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

#63738701
def pixiv_id_request(bot, update):
    update.message.reply_text("give me pixiv pic id")
    return 1
def pixiv_id_proc(bot, update):
    update.message.reply_text("searching...")
    pic_get=pixiv_auto_get.pixiv_auto_get(pixiv_id=update.message.text)
    if not pic_get is None:
        for pic_pos in pic_get:
            update.message.reply_photo(open(pic_pos,"rb"))
    else:
        update.message.reply_text("Not Found or Error")
    return ConversationHandler.END

def cognitive_description_request(bot,update):
    update.message.reply_text("give me a photo")
    return 1
def cognitive_description_proc(bot,update):
    user=update.message.from_user
    photo_file=bot.get_file(update.message.photo[-1].file_id)
    photo_file.download("test_photo.jpg")
    logger.info("Photo of %s: %s" % (user.first_name, 'test_photo.jpg'))
    output=description.Description('test_photo.jpg')
    update.message.reply_text(output)
    return ConversationHandler.END

def cognitive_ocr_request(bot,update):
    update.message.reply_text("give me a photo")
    return 1
def cognitive_ocr_proc(bot,update):
    user=update.message.from_user
    photo_file=bot.get_file(update.message.photo[-1].file_id)
    photo_file.download("test_photo.jpg")
    logger.info("Photo of %s: %s" % (user.first_name, 'test_photo.jpg'))
    output=ocr.OCR('test_photo.jpg')
    update.message.reply_text(output)
    return ConversationHandler.END

def start_mail_request(bot,update):
    print(update.message.from_user.id)
    if not os.path.exists("mail_config"):
        print(1)
        os.makedirs("mail_config")
        os.makedirs("mail_content")
    file_name='mail_config/'+str(update.message.from_user.id)+'.json'
    if os.path.exists(file_name):
        update.message.reply_text("input the content")
        return 2
    else:
        update.message.reply_text("""please setup your mail config\nFormat:\nsmtp_host;pop_host;mail_address;password""")
        return 1

def clear_mail_config(bot,update):
    file_name='mail_config/'+str(update.message.from_user.id)+'.json'
    if not os.path.exists(file_name):
        update.message.reply_text("no config")
    else:
        os.remove(file_name)
        update.message.reply_text("clear")
    return ConversationHandler.END

def setup_mail_config(bot,update):
    file_name='mail_config/'+str(update.message.from_user.id)+'.json'
    print(update.message.text)
    config_list=update.message.text.split(";")
    config_dict={}
    config_dict['smtp_host']=config_list[0]
    config_dict['pop_host']=config_list[1]
    config_dict['mail_address']=config_list[2]
    config_dict['password']=config_list[3]
    config_str=json.dumps(config_dict)
    with open(file_name,'w') as f:
        f.write(config_str)
        f.close()
    update.message.reply_text("config complete, input content")
    return 2
def edit_mail_content(bot,update):
    file_name='mail_content/'+str(update.message.from_user.id)+'_draft.txt'
    f=open(file_name,"w")
    f.write(update.message.text)
    update.message.reply_text("content complete")
    update.message.reply_text("input title and address\nformat:\ntitle;address")
    #update.message.reply_text("add a document, or input /skip to skip")
    return 3
def send_mail_proc(bot,update):
    title,address=update.message.text.split(";")
    content=""
    f=open('mail_content/'+str(update.message.from_user.id)+'_draft.txt','r')
    content=f.read()
    f.close()
    config=json.loads(open('mail_config/'+str(update.message.from_user.id)+'.json','r').read())
    try:
        status=mail.send(smtp_host=config['smtp_host'],mail_user=config['mail_address'],mail_pass=config['password'],to_list=[address],subject=title,text=content)
        if status==True:
            update.message.reply_text("sent")
        else:
            update.message.reply_text("failed")
    except Exception as e:
        print(e)
        update.message.reply_text("failed")
    return ConversationHandler.END

def shortlink_request(bot,update):
    update.message.reply_text("give me a link")
    return 1
def shortlink_proc(bot,update):
    update.message.reply_text(shortlink.shortlink(update.message.text))
    return ConversationHandler.END

def weather_request(bot,update):
    update.message.reply_text("give me a city name")
    return 1
def weather_proc(bot,update):
    update.message.reply_text(weatherinfo.weatherinfo(update.message.text))
    return ConversationHandler.END

def translate_request(bot,update):
    if not os.path.exists('translate'):
        os.makedirs('translate')
    update.message.reply_text('input the target language in short')
    update.message.reply_text(translate.lang_list)
    return 1
def lang_proc(bot,update):
    if not os.path.exists('translate'):
        os.makedirs('translate')
    f=open('translate/'+str(update.message.from_user.id)+'.txt','w')
    f.write(update.message.text)
    f.close()
    update.message.reply_text('give me the content to be translated')
    return 2
def content_proc(bot,update):
    if not os.path.exists('translate'):
        os.makedirs('translate')
    content=update.message.text
    lang=open('translate/'+str(update.message.from_user.id)+'.txt','r').read()
    update.message.reply_text(translate.translate(q=content,toLang=lang))
    return ConversationHandler.END

def repeat(bot,update):
    update.message.reply_text(update.message.text)
# def chinese_debug(bot,update):
#     print(update.message.text)
def query_natural_lang(bot,update):
    if update.message.chat.type != "private":
        return ConversationHandler.END
    ans = qna.qna_request(update.message.text)
    if ans == "No good match found in the KB":
        return ConversationHandler.END
    elif ans == "command:mail":
        return QNA_COMMAND_MAIL
    elif ans == "command:pixiv":
        update.message.reply_text("give me pixiv pic id")
        return QNA_COMMAND_PIXIV
    elif ans == "command:ocr":
        update.message.reply_text("give me a photo")
        return QNA_COMMAND_OCR
    elif ans == "command:description":
        update.message.reply_text("give me a photo")
        return QNA_COMMAND_DESCRIPTION
    elif ans == "command:btdigg":
        update.message.reply_text("input the  search content")
        return QNA_COMMAND_BTDIGG
    elif ans == "command:shortlink":
        update.message.reply_text("give me a link")
        return QNA_COMMAND_SHORTLINK
    elif ans == "command:translate":
        update.message.reply_text("input the language")
        update.message.reply_text(translate.lang_list)
        return QNA_COMMAND_TRANSLATE
    elif ans == "command:weather":
        update.message.reply_text("give me the city name in Chinese")
        return QNA_COMMAND_WEATHER
    elif ans == "command:song":
        update.message.reply_text("give me the song name")
        return QNA_COMMAND_SONG
def do_nothing(bot,update):
    pass
def song_request(bot,update):
    update.message.reply_text('give me the name of song')
    return 1
def song_proc(bot,update):
    Netease=netease_music_lib.NeteaseMusic()
    info = Netease.get_song_info_by_name(update.message.text)
    link = info[-1]
    if not link==None:
        data=urllib.request.urlopen(link).read()
        fileName = link.split("/")[-1]
        print(fileName)
        with open(fileName,"wb") as f:
            f.write(data)
            f.close()
        with open(fileName,"rb") as f:
            bot.send_audio(update.message.chat_id,audio=f,title=info[1],performer=info[2],timeout=60)
        #print(link)

    else:
        update.message.reply_text('could not fetch this song')
    return ConversationHandler.END
def nhentai_request(bot,update):
    update.message.reply_text("send random to get random manga, send id to download specific manga, send search to find manga with some keywords, send popsearch to find manga with popular rate descending order")
    return 1
def nhentai_proc(bot,update):
    content=update.message.text
    if content == "id":
        update.message.reply_text("input manga id")
        return 2
    elif content == "random":
        nhentai = NHentai.NHentai()
        random_book = nhentai.refresh_random()
        random_book.download_all()
        download_path = random_book.pack()
        if not download_path is None:
            with open(download_path,"rb") as f:
                bot.send_document(update.message.chat_id,document=f,filename=random_book.title_eng)
        return ConversationHandler.END
    elif content == "search":
        update.message.reply_text("input search content")
        return 3
    elif content == "popsearch":
        update.message.reply_text("input search content")
        return 4
def nhentai_id_proc(bot,update):
    content=update.message.text
    if content.isdigit():
        book = NHentai.Book(content)
        book.download_all()
        download_path = book.pack()
        if not download_path is None:
            with open(download_path,"rb") as f:
                bot.send_document(update.message.chat_id,document=f,filename=random_book.title_eng)
    else:
        update.message.reply_text("invalid id")
    return ConversationHandler.END
def nhentai_search_proc(bot,update):
    content=update.message.text
    content = content.replace(" ", "+")
    nhentai = NHentai.NHentai()
    result = nhentai.search(query=content,is_popular=False)
    rep_str = ""
    for _id, title in result:
        rep_str += " -> ".join([str(_id),str(title)]) + "\n"
    update.message.reply_text(rep_str)
    return ConversationHandler.END
def nhentai_popsearch_proc(bot,update):
    content=update.message.text
    content = content.replace(" ", "+")
    nhentai = NHentai.NHentai()
    result = nhentai.search(query=content,is_popular=True)
    rep_str = ""
    for _id, title in result:
        rep_str += " -> ".join([str(_id),str(title)]) + "\n"
    update.message.reply_text(rep_str)
    return ConversationHandler.END


#Main function
def main():
    updater=Updater("your config")
    dp=updater.dispatcher

    btdigg_conv_handler=ConversationHandler(entry_points=[CommandHandler("btdigg",btdigg_start)],
    states={
        1:[MessageHandler(Filters.text,btdigg_get)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
    )

    pixiv_get_conv_handler=ConversationHandler(entry_points=[CommandHandler("pixiv",pixiv_id_request)],
    states={
    1:[MessageHandler(Filters.text,pixiv_id_proc)]
    },fallbacks=[CommandHandler('cancel', cancel)])

    description_conv_handler=ConversationHandler(entry_points=[CommandHandler("description",cognitive_description_request)],
    states={
        1:[MessageHandler(Filters.photo,cognitive_description_proc)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
    )

    ocr_conv_handler=ConversationHandler(entry_points=[CommandHandler("ocr",cognitive_ocr_request)],
    states={
        1:[MessageHandler(Filters.photo,cognitive_ocr_proc)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
    )

    mail_send_handler=ConversationHandler(entry_points=[CommandHandler("mail",start_mail_request)],
    states={
        1:[MessageHandler(Filters.all,setup_mail_config)],
        2:[MessageHandler(Filters.all,edit_mail_content)],
        3:[MessageHandler(Filters.all,send_mail_proc)]
    },
    fallbacks=[CommandHandler('cancel', cancel)])

    short_link_handler=ConversationHandler(entry_points=[CommandHandler("shortlink",shortlink_request)],
    states={
    1:[MessageHandler(Filters.text,shortlink_proc)]
    },
    fallbacks=[CommandHandler('cancel', cancel)])

    nhentai_handler=ConversationHandler(entry_points=[CommandHandler("nhentai",nhentai_request)],
    states={
    1:[MessageHandler(Filters.text,nhentai_proc)],
    2:[MessageHandler(Filters.text,nhentai_id_proc)],
    3:[MessageHandler(Filters.text,nhentai_search_proc)],
    4:[MessageHandler(Filters.text,nhentai_popsearch_proc)],
    },
    fallbacks=[CommandHandler('cancel', cancel)])

    weather_info_handler=ConversationHandler(entry_points=[CommandHandler("weather",weather_request)],
    states={
    1:[MessageHandler(Filters.text,weather_proc)]
    },
    fallbacks=[CommandHandler('cancel', cancel)])

    translate_handler=ConversationHandler(entry_points=[CommandHandler("translate",translate_request)],
    states={
    2:[MessageHandler(Filters.text,content_proc)],
    1:[MessageHandler(Filters.text,lang_proc)]
    },
    fallbacks=[CommandHandler('cancel', cancel)])

    song_handler=ConversationHandler(entry_points=[CommandHandler("song",song_request)],
    states={
        1:[MessageHandler(Filters.text,song_proc)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
    )

    echo_handler = ConversationHandler(entry_points=[CommandHandler("echo",echo_request)],states={},fallbacks=[CommandHandler('cancel',cancel)])

    natural_lang_handler = ConversationHandler(entry_points=[MessageHandler(Filters.text,query_natural_lang)],states={
        QNA_COMMAND_TRANSLATE:[MessageHandler(Filters.text,qna.lang_proc)],
        QNA_COMMAND_TRANSLATE+1:[MessageHandler(Filters.text,qna.content_proc)],
        QNA_COMMAND_BTDIGG:[MessageHandler(Filters.text,qna.btdigg_get)],
        QNA_COMMAND_SHORTLINK:[MessageHandler(Filters.text,qna.shortlink_proc)],
        QNA_COMMAND_WEATHER:[MessageHandler(Filters.text,qna.weather_proc)],
        QNA_COMMAND_OCR:[MessageHandler(Filters.photo,qna.cognitive_ocr_proc)],
        QNA_COMMAND_SONG:[MessageHandler(Filters.text,qna.song_proc)],
        QNA_COMMAND_DESCRIPTION:[MessageHandler(Filters.photo,qna.cognitive_description_proc)]
    },
    fallbacks=[CommandHandler('cancel',cancel)])

    dp.add_handler(echo_handler)
    dp.add_handler(mail_send_handler)
    dp.add_handler(btdigg_conv_handler)
    dp.add_handler(pixiv_get_conv_handler)
    dp.add_handler(description_conv_handler)
    dp.add_handler(ocr_conv_handler)
    dp.add_handler(short_link_handler)
    dp.add_handler(weather_info_handler)
    dp.add_handler(translate_handler)
    dp.add_handler(song_handler)
    dp.add_handler(CommandHandler("start",start))
    dp.add_handler(CommandHandler("clearmailconfig",clear_mail_config))
    dp.add_handler(natural_lang_handler)
    dp.add_handler(nhentai_handler)
    #dp.add_handler(RegexHandler(r"/cn.+?",chinese_debug))
    #dp.add_handler(RegexHandler(r"/pixiv.+?",pixivget))
    #dp.add_handler(MessageHandler(Filters.photo,photo))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__=="__main__":
    main()
