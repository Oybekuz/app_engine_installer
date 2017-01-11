#!/usr/bin/env python
#-*-coding:utf8;-*-

project_name = "project_nomi" 
import fileworker as fv
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import logging
import threading
import requests
import json
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import telebot
import time
from time import sleep
from telebot import types
import os
import random
from datetime import datetime
from pytz import timezone
import webapp2
import urllib
import urllib2
API_TOKEN = "replace_me_with_token"
def admin(user_id):
    Admins = [88505037, 8768957689476] #Adminlar id si ro'yhati. Bu yerga o'zingizni id raqamingizni yozing. Tel raqam emas, telegramdagi id raqam
    if user_id in Admins:
        return(True)
    else:
        return(False)
bot=telebot.TeleBot(API_TOKEN, threaded=False)
bot_id=API_TOKEN.split(":")[0]

def _print(a):
    logging.info(str(a))
    return

def md(txt):
    return(txt.replace("_","\_").replace("*","\*").replace("`","\`").replace("[","\["))

class Knowledge(ndb.Model):  
    answer = ndb.StringProperty()

def get_answer(text):
    s = Knowledge.get_by_id(text.decode('utf-8'))
    if s: 
        if "|" in s.answer:
            return(random.choice(s.answer.split('|')))
        else:
            return(s.answer)

def get_all_answers(text):
    s = Knowledge.get_by_id(text)
    if s: 
        return(s.answer)
    return("")
    
def add_answer(text, answer):
    text=text.decode('utf-8')
    answers = get_all_answers(text.decode('utf-8'))
    if len(answers)>0:
        answers = answers.split("|")
    else:
        answers = []
    answers=answers.append(text)
    s = Knowledge.get_or_insert("|".join(answers))
    s.answer = answer.decode('utf-8') 
    s.put()
    
def broadcast(data):
    subscribe = fv.open('./enabled_list.uzsdb', 'r').read().split('\n')
    subscribe_count = len(subscribe)
    yi = 0
    i = 0
    while i < subscribe_count:
        try:
            bot.send_message(int(subscribe[i]), data)
            yi = yi + 1
        except Exception as e:
            _print("Foydalanuvchi " + str(subscribe[i]) + " ga hat yetib bormadi")
        i = i + 1
    return(yi)
        
def getEnabled(chatid):
    try:
        fv.open('./enabled_list.uzsdb', 'r').read().split('\n').index(str(chatid))
        return True
    except:
        return False
    
def setEnabled(chatid, enable=True):
    enable_list = fv.open('./enabled_list.uzsdb', 'r').read().split('\n')
    if enable:
        enable_list.append(str(chatid))
    else:
        try:
            enable_list.remove(str(chatid))
        except:
            'ok'
    fv.open('./enabled_list.uzsdb', 'w').write('\n'.join(enable_list))
    return

def next_step(chatid, stepstr):
    fv.open('./users/info_' + str(chatid) + '.uzsdb', 'w').write(stepstr)
    

@bot.message_handler(func=lambda message: True, content_types=['new_chat_member'])
def new_chat_member(message):
    chat_id = message.chat.id #gruppani telegramdagi id si
    try:
        user_id = message.new_chat_member.id
    except:
        user_id = message.from_user.id
    #user_id - gruppaga qo'shilgan odam id si. Shunchaki ma'lumot uchun
    if message.new_chat_member.first_name:
        first_name=message.new_chat_member.first_name
    else:
        first_name=message.from_user.first_name
    #first_name - foydalanuvchi ismi. Shunchaki ma'lumot uchun 
    username = "None"
    if message.new_chat_member.username:
        username = message.new_chat_member.username
    
    if not(username.lower().endswith('bot')):
        bot.send_message(chat_id, "Salom, " + first_name)

@bot.message_handler(func=lambda message: True)
def main(message):
    first_name = message.from_user.first_name.decode("utf-8") #hat yozgan odam ismi
    user_id = message.from_user.id #hat yozgan odam id si
    chat_id = message.chat.id #chat id si. Agar gruppa bo'sa chat_id<0, agar lichka bo'sa user_id bilan bir xil
    text = str(message.text).decode("utf-8") #yozilfan gat matni
    if len(text)>0: #agar text uzunligi 0 dan kotta bo'sa (hatolarni oldini olish uchun
        try:
            if chat_id>0: #lichka bo'sa
                step = fv.open('./users/info_' + str(chat_id) + '.uzsdb', 'r').read()
            else: #gruppa bo'sa
                step = "group_chat"
        except:
            step = 'none'
        
        def start():
            if getEnabled(chat_id): #agar oldin yozgan bo'sa
                bot.send_message(chat_id, "Salom, qalesiz?")
                next_step(chat_id, 'main')
            else:
                setEnabled(chat_id)
                bot.send_message(chat_id, "*Salom, siz bu botga a'zo bo'ldingiz*", parse_mode="Markdown", disable_web_page_preview=True) #so'zni to'g'illavolasila
                try:
                    history = fv.open('./history.uzsdb', 'r').read().split('|')
                except:
                    history = ["0"]
                next_step(chat_id, 'main')
                if history.count(str(chat_id)) == 0:
                    history.append(str(chat_id))
                    fv.open('./history.uzsdb', 'w').write('|'.join(history))
            return
        
        if admin(chat_id): #agar admin yozsa
            if text.startswith("/send_id_"):
                try:
                    bot.send_message(text.replace("/send_id_","").split(" ",1)[0], text.replace("/send_id_","").split(" ",1)[1], parse_mode="Markdown")
                    bot.send_message(chat_id, "Etip qo'ydim )")
                except Exception as ex:
                    bot.send_message(chat_id, "Hat yetip bormadi. Hato: " + str(ex))
            
            if text.startswith('/learn '):
                try:
                    bot.send_message(chat_id, "Buyruqlarni o'rganish uchun /learn_help")
                    data = text.split(' ',1)[1]
                    if '|' in data:
                        savol = data.split('|',1)[0]
                        answer = data.split("|",1)[1]
                        if len(savol)<20:
                            add_answer(savol, answer)
                            bot.send_message(chat_id, "O'rganib oldim.")
                        else:
                            bot.send_message(chat_id, "Savol juda uzun")
                    else:
                        bot.send_message(chat_id, "*/learn salov|javob* ko'rinishida yozing!", parse_mode="Markdown")
                except Exception as ex:
                    
                    bot.send_message(chat_id, "*/learn salov|javob* ko'rinishida yozing!\n" + str(ex), parse_mode="Markdown")
            
            elif text == "/learn_help":
                bot.send_message(chat_id, "Salom, siz bo'tga so'z o'rgatishiz uchun quyidagi shakilda buyruq bering: \n/learn So'z|javob \n misol uchun siz 'Salom' so'ziga 'Salom, ishla qale' deb javob berishni o'rgatmoxchi bo'lsangiz quyidagi buyruqni berasiz. \n/learn Salom|Salom, ishla qale?\nO'rgatilgan so'zla bazadan o'chirilishi hali qo'shilgani yo'q. Shuning uchun so'zlarni yaxshilap o'ylap qo'shing.")
                bot.send_message(chat_id, "Misol uchun agar menga 'kim man' dip yozsa, man uni otini yozishim kere bo'sa, quyidagicha buyruq berasiz: \n/learn kim man|Sizni telegramdagi ismingiz: __name__ \nta'ni ikkita '_' chizig'i name va yana ikkita __ chiziq. Bu boshqa so'zlaga aralaship ketmasligi uchun. Bundan tashqari, siz __id__ buyrug'iniyam ishlatishingiz mummin. Misol uchun:\n/learn /id|__id__\bBularni sinap ko'ring.")
                

        if text.startswith("/start"):
            start()
                
        
        elif step == "group_chat":
            if text=="salom" or text=="Salom" or text=="салом" or text=="Салом":
                Salom =["Salooom!",
                        "Salom, qalesiz",
                        "Tekinakan db salom bervurasizmi endi, qalesiz o'zi tinchmi! 😜",
                        "Va aleykum assalom bo'tam",
                        "Salom!"] #shu joyga hohlaganizzi yozin
                r_salom=random.choice(Salom)
                bot.reply_to(message, r_salom)
            
            elif text=="ok":
                bot.reply_to(message,"ok") #bu tomoni yana example
            elif text == "/markdown":
                bot.send_message(chat_id, "*BOLD*, _italic_, `fixedsys`, [giperssilka](https://telegram.me/uzstudio)", parse_mode="Markdown")
            
            
            elif text.startswith("/screen "):
                text = text.split(" ",1)[1]
                if text.startswith("http") and not " " in text:
                    try:
                        data = urllib2.urlopen("https://screenshotmachine.com/processor.php?urlparam=" + urllib.quote(text)).read()
                        data = data.replace(data[:(data.find("href='") + len("href='"))],"")
                        data = data[:data.find("'")]
                        data = "https://screenshotmachine.com/" + data
                        try:
                            bot.send_photo(chat_id, data)
                        except:
                            bot.send_message(chat_id, "[screenshot](" + str(data) + ") topilmadi", parse_mode="Markdown")
                    except:
                        _print(" ")
            
            
            else:
                if "-" in text or "+" in text or "^" in text or "*" in text or "/" in text or "!" in text or ":" in text:
                    exp = text
                    try:
                        data = urllib2.urlopen("http://api.mathjs.org/v1/?expr=" + urllib.quote(exp)).read()
                        bot.send_message(chat_id, str(data))
                    except Exception as ex:
                        logging.info(ex)
                
                if len(text)<20:
                    answer = get_answer(text)
                    if answer:
                        bot.send_message(chat_id, answer.replace('__name__', first_name).replace('__id__', str(message.from_user.id)))
            
            
                    

        elif step=="none":
            start()
                    
        elif text == "/ping": #bot tezligini aniqlash uchun
            bot.send_chat_action(chat_id, 'typing')
            m = bot.send_message(chat_id, "pong")
            ping = time.time() - message.date
            bot.edit_message_text("ping=" + str(ping), chat_id=chat_id, message_id=m.message_id)
            #bot.send_chat_action(chat_id, 'typing')
        
        elif text == "/about": #Agar foydalanuvchilarni hisoblash sistemasini 0 dan tuzsangiz, @UzStudio ni optashasiz mumkin
            chats = fv.open('./enabled_list.uzsdb', 'r').read().split('\n')
            i = 0
            group = 0
            while i < len(chats):
                if chats[i].startswith('-'):
                    group = group + 1
                i = i + 1
            chats = len(chats) - group
            keyboard = types.InlineKeyboardMarkup()
            callback = types.InlineKeyboardButton(text="♻️Yangilash♻️", callback_data="about_yangilash")
            keyboard.add(callback)
            subscribe_about = '📈Bot foydalanuvchilari:\n👤*' + str(chats) + '* odamlar,\n👥*' + str(group) + '* guruxlar.\n🕵Hammasi bo\'lip: *' + str(chats+group) + '*\n'
            bot.send_message(chat_id, subscribe_about +"\n*" +   str(time.time()) + "*\n\n©`2015`-`2016` @UzStudio ™", parse_mode="Markdown")

        elif step=="main": #Agar asosiy menyuda bo'lsa
            if text=="/command" or text == "command":
                bot.send_message(chat_id, "answer")
            
            elif text == "/help" or text == "Yordam⁉️": 
                bot.send_chat_action(chat_id, 'typing') #typing chiqarish
                bot.send_message(chat_id, "Salom, bu bot gruppalada va lichkada sal boshqacharoq gaplashadi. Bo't qilolidiganishlari:\n1) Misollar yechish. lichkamga har-hil misollar berib ko'ringlar. 2) Saytlarni screenshot qilish. gruppada buyruqga misol: /screen http://gruppala.ga/ lichkada shundo sayt urlsi yoziladi. \nBo't Admin o'rgatgan so'zlaniaym o'rgana oladi.") #davomini yozarsiz
            
            elif text.startswith("/echo"):
                try:
                    data = text.split(" ",1)[1]
                    bot.send_message(chat_id, data)
                except:
                    bot.send_message(chat_id, "/echo qanaqadir text")
                    
            else:
                if "-" in text or "+" in text or "^" in text or "*" in text or "/" in text or "!" in text or ":" in text:
                    exp = text
                    try:
                        data = urllib2.urlopen("http://api.mathjs.org/v1/?expr=" + urllib.quote(exp)).read()
                        bot.send_message(chat_id, str(data))
                    except Exception as ex:
                        logging.info(ex)
                if len(text)<20:
                    answer = get_answer(text)
                    if answer:
                        bot.send_message(chat_id, answer.replace('__name__', first_name).replace('__id__', str(message.from_user.id)))
                        
                if text.startswith("http") and not " " in text:
                    try:
                        data = urllib2.urlopen("https://screenshotmachine.com/processor.php?urlparam=" + urllib.quote(text)).read()
                        data = data.replace(data[:(data.find("href='") + len("href='"))],"")
                        data = data[:data.find("'")]
                        data = "https://screenshotmachine.com/" + data
                        try:
                            bot.send_photo(chat_id, data)
                        except:
                            bot.send_message(chat_id, "[screenshot](" + str(data) + ") topilmadi", parse_mode="Markdown")
                    except:
                        _print(" ")
                
                    
            
                
            
        
    return


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

# webserver index
class IndexHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write("""<!DOCTYPE html>
<html lang="uz">
  <head>
    <meta charset="utf-8">
    <title>gruppala_bot</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content=""" + project_name +""" " serveri">
    <meta name="author" content="UzStudio">
  <link rel="shortcut icon" href="/favicon.ico">

  </head>
  <body>

 <h1><a href="tg:reslove?domain=uzstudio">""" + project_name + """</a> ning serveri</h1>
 </body>
</html>""")
        return


  # bu joyiga teymela!!! Eng optimal qilip yozib bo'lingan!
# Process webhook calls
class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(600)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        try:
            json_string = json.loads(self.request.body.decode("utf-8"))
            updates = [telebot.types.Update.de_json(json_string)]
            new_messages = []
            edited_new_messages = []
            new_inline_querys = []
            new_chosen_inline_results = []
            new_callback_querys = []
            for update in updates:
                if update.message:
                    new_messages.append(update.message)
                if update.edited_message:
                    edited_new_messages.append(update.edited_message)
                if update.inline_query:
                    new_inline_querys.append(update.inline_query)
                if update.chosen_inline_result:
                    new_chosen_inline_results.append(update.chosen_inline_result)
                if update.callback_query:
                    new_callback_querys.append(update.callback_query)
            logger.debug('Received {0} new updates'.format(len(updates)))
            if len(new_messages) > 0:
                bot.process_new_messages(new_messages)
            if len(edited_new_messages) > 0:
                bot.process_new_edited_messages(edited_new_messages)
            if len(new_inline_querys) > 0:
                bot.process_new_inline_query(new_inline_querys)
            if len(new_chosen_inline_results) > 0:
                bot.process_new_chosen_inline_query(new_chosen_inline_results)
            if len(new_callback_querys) > 0:
                bot.process_new_callback_query(new_callback_querys)    
        except Exception as ex:
            logging.error(str(ex))
        self.response.write('{"ok": true}')
        return
        
            
        


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get("url")
        try:
            fv.open("./enabled_list.uzsdb","r").read()
        except:
            fv.open('./enabled_list.uzsdb',"w").write("0")
        
        try:
            fv.open("./history.uzsdb","r").read()
        except:
            fv.open('./history.uzsdb',"w").write("0")
            
        if not url:
            bot.set_webhook("https://" + project_name + ".appspot.com/webhook")
        else:
            bot.set_webhook(url)
        self.response.write("ok")
        return
        
app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
