#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr,parsedate

"""
functions:
send_mail(to_list,subject,text=None,image=None,attachment=None)	return bool
receive_mail(Subject=None,From=None,Timeperiod=None)	return msg(object)
print_info(msg,indent=0)	return None
get_texts(msg)	return text(str)


please complete your mail info in this code
smtp_host=#"smtp.126.com"
pop_host=#"pop.126.com"
mail_user=
mail_pass=
mail_from="Akaisora<%s>"%mail_user
"""


# smtp_host=#"smtp.126.com"
# pop_host=#"pop.126.com"
# mail_user=
# mail_pass=
# mail_from="Akaisora<%s>"%mail_user
def send(smtp_host,mail_user,mail_pass,to_list,subject,text=None,image=None,attachment=None):
	"""to_list=list/str   subject=str   text=list/str/None   image=list/str/None   attachment=list/str/None"""
	if not isinstance(to_list,(list,tuple)):to_list=[to_list]

	msg=MIMEMultipart('mixed')
	msg["Subject"]=subject
	msg["From"]=mail_user
	msg["To"]=";".join(to_list)

	try:
		msgRelated=MIMEMultipart('related')
		msg.attach(msgRelated)
		msgAlternative=MIMEMultipart('alternative')
		msgRelated.attach(msgAlternative)

		if text!=None:				#添加文字
			msgAlternative.attach(MIMEText(text,"html","utf-8"))

		if image!=None:				#添加图片
			img_list=image if isinstance(image,(list,tuple)) else [image]
			for filename in img_list:
				img_html="<p><img src='cid:image%d'></p>"%img_list.index(filename)
				msgAlternative.attach(MIMEText(img_html,"html","utf-8"))

				msgImage=MIMEImage(open(filename,'rb').read())
				msgImage["Content-ID"]="<image%d>"%img_list.index(filename)
				msgImage["Content-Disposition"]="attachment; filename="+os.path.basename(filename)
				msgRelated.attach(msgImage)

		if attachment!=None:		#添加附件
			att_list=attachment if isinstance(attachment,(list,tuple)) else [attachment]
			for filename in att_list:
				msgAtt=MIMEText(open(filename,'rb').read(),'base64','utf-8')
				msgAtt["Content-Type"]="application/octet-stream"
				msgAtt["Content-Disposition"]="attachment; filename="+os.path.basename(filename)
				msg.attach(msgAtt)

		#连接服务器，发送邮件
		server=smtplib.SMTP_SSL(smtp_host,465)
		server.login(mail_user,mail_pass)
		server.sendmail(mail_user,to_list,msg.as_string())
		server.quit()
		return True
	except Exception as e:
		print(e)
		return False

def send_mail(to_list,subject,text=None,image=None,attachment=None):
	"""to_list=list/str   subject=str   text=list/str/None   image=list/str/None   attachment=list/str/None"""
	if not isinstance(to_list,(list,tuple)):to_list=[to_list]

	msg=MIMEMultipart('mixed')
	msg["Subject"]=subject
	msg["From"]=mail_from
	msg["To"]=";".join(to_list)

	try:
		msgRelated=MIMEMultipart('related')
		msg.attach(msgRelated)
		msgAlternative=MIMEMultipart('alternative')
		msgRelated.attach(msgAlternative)

		if text!=None:				#添加文字
			msgAlternative.attach(MIMEText(text,"html","utf-8"))

		if image!=None:				#添加图片
			img_list=image if isinstance(image,(list,tuple)) else [image]
			for filename in img_list:
				img_html="<p><img src='cid:image%d'></p>"%img_list.index(filename)
				msgAlternative.attach(MIMEText(img_html,"html","utf-8"))

				msgImage=MIMEImage(open(filename,'rb').read())
				msgImage["Content-ID"]="<image%d>"%img_list.index(filename)
				msgImage["Content-Disposition"]="attachment; filename="+os.path.basename(filename)
				msgRelated.attach(msgImage)

		if attachment!=None:		#添加附件
			att_list=attachment if isinstance(attachment,(list,tuple)) else [attachment]
			for filename in att_list:
				msgAtt=MIMEText(open(filename,'rb').read(),'base64','utf-8')
				msgAtt["Content-Type"]="application/octet-stream"
				msgAtt["Content-Disposition"]="attachment; filename="+os.path.basename(filename)
				msg.attach(msgAtt)

		#连接服务器，发送邮件
		server=smtplib.SMTP_SSL(smtp_host,465)
		server.login(mail_user,mail_pass)
		server.sendmail(mail_user,to_list,msg.as_string())
		server.quit()
		return True
	except Exception as e:
		print(e)
		return False

def receive_mail(Subject=None,From=None,Timeperiod=None):
	"""Subject,Form is used to filter mails, when find more than one mail, it will choose the latest"""
	try:
		server=poplib.POP3_SSL(pop_host,995)
		# print(server.getwelcome().decode('utf-8'))
		server.user(mail_user)
		server.pass_(mail_pass)

		print("message: %s. Size: %s"%server.stat())

		resp,mails,octets=server.list()
		# print(mails)

		mail_amount=len(mails)
		msg=None
		if Timeperiod:datepoint=datetime.datetime.now()-datetime.timedelta(seconds=Timeperiod)
		for index in range(mail_amount,0,-1):
			resp,lines,octets=server.top(index,0)
			msg_content=b'\r\n'.join(lines).decode('utf-8')
			msg=Parser().parsestr(msg_content)

			if Timeperiod and datetime.datetime(*parsedate(msg.get("Date"))[:6])<datepoint:break

			msgFrom=_decode_str(parseaddr(msg.get("From"))[0])+"<%s>"%parseaddr(msg.get("From"))[1]
			msgSubject=_decode_str(msg.get("Subject"))

			if (From==None or (From in msgFrom)) and (Subject==None or (Subject in msgSubject)):
				resp,lines,octets=server.retr(index)
				msg_content=b'\r\n'.join(lines).decode('utf-8')
				msg=Parser().parsestr(msg_content)
				print("retr index ",index)
				break

		# print_info(msg)
		# print("".join(get_texts(msg)))
		server.quit()

		return msg
	except Exception as e:
		print(e)
		return None

def print_info(msg,indent=0):
	"""print the msg content in a nice format"""
	if indent==0:
		for header in ['From','To','Subject']:
			value=msg.get(header,'')
			if value:
				if header=='Subject':
					value=_decode_str(value)
				else:
					hdr,addr=parseaddr(value)
					name=_decode_str(hdr)
					value="%s<%s>"%(name,addr)
			print("%s%s: %s"%('  '*indent,header,value))
	if(msg.is_multipart()):
		parts=msg.get_payload()
		for n,part in enumerate(parts):
			print("%spart %s"%('  '*indent,n))
			print("%s-----------------"%('  '*indent))
			print_info(part,indent+1)
	else:
		content_type=msg.get_content_type()
		if content_type in {'text/plain','text/html'}:
			content=msg.get_payload(decode=True)
			charset=_guess_charset(msg)
			if charset:
				content=content.decode(charset)
			print('%sText: %s'%('  '*indent,content))
		else:
			filename=msg.get("Content-Disposition","")
			pos=filename.find("filename")
			filename=filename[pos:] if pos>=0 else ""
			print('%sAttachement: %s %s'%('  '*indent,content_type,filename))

def get_texts(msg):
	"""get all text type content in the mail as a list of str"""
	ret=[]
	if(msg.is_multipart()):
		parts=msg.get_payload()
		for part in parts:
			ret+=get_texts(part)
	else:
		content_type=msg.get_content_type()
		if content_type in {'text/plain','text/html'}:
			content=msg.get_payload(decode=True)
			charset=_guess_charset(msg)
			if charset:
				content=content.decode(charset)
			ret+=[content]
	return ret

def get_from_add(msg):
	return parseaddr(msg.get("From"))[1]

def _decode_str(s):
	value,charset=decode_header(s)[0]
	if charset:
		value=value.decode(charset)
	return value

def _guess_charset(msg):
	charset=msg.get_charset()
	if charset is None:
		content_type=msg.get('Content-Type','').lower()
		pos=content_type.find('charset=')
		if pos>=0:
			charset=content_type[pos+8:].strip().split()[0].strip().strip(';\'"')
	return charset




if __name__=="__main__":
	test_to_list=mail_user
	if send_mail(test_to_list,"测试邮件","Welcome to <a href='http://akaisora.tech'>Akaisora's blog</a>","test.png","fuck.txt"):
		print("发送成功")
	else:
		print("发送失败")

	import time
	time.sleep(5)

	msg=receive_mail(Subject="测试邮件")
	if msg:
		print_info(msg)
		print("接收成功")
	else:
		print("接收失败")
