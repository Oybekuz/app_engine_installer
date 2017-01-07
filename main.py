#!/user/bin/python
#-*-coding:utf-8-*-
import os
import threading
import urllib2
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def a():
    data = urllib2.urlopen("https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.38.zip").read()
    open('./master.zip',"w").write(data)
    data = ""
    
threading.Thread(target=a).start()

def wait(instruction):
    while raw_input("O'xshadimi? y/n:").lower() != "y":
        print(instruction)

print("Salom, bu script sizga google ga bo't joylashga yordam beradi. 1) appengine.google.com ga kiring. Kirganingizda \"y\" dip yozing.")
while raw_input("Kirdingizmi? y/n:").lower() != "y":
    print('https://appengine.google.com/ ga kiring. Bu qiyinamas')

print("Ok. Kirgan bo'lsangiz, u yerda \033[4m'Create project'\033[0m yoki \033[4m'Создать проект'\033[0m tugmasini bosing. Bosgandan keyin yana 'y' ni bosing.")
wait("Yaxshilap e'tibor bilan qidiring. Script topib beomidi. Topsangiz, 'y' jo'nating")
print("Menyu ochiladi, va u yerga project nomini yozasiz. Yaxshisi, bo'tingizni userneymini yozing. Misol uchun, @intelekt_bot ni intelekt-bot deb, shunda chalkashishlar kam bo'ladi.")
print("\033[1m Project nomi bila id si bir xil bo'lgani yaxshi. Project nomi va id sini eslap qoling!\033[0m")
print('proektni sozdat qilishni bosing. Pasda "creating project..." yoki shunga o\'xshagan yozuv chiqadi')
wait("Project nomini va id sini eslap qolip, create yoki \033[95mсоздать\033[0m ni \033[95mbosing\033[0m")
print("Endi workspace ni tayorlimiza. Ungacha google proekt tayyorlab turadi. faylla orasida master.zip paydo bo'ldimi?")
while raw_input("y/n:").lower() != "y":
    print("Ozgina kuting va yana qarang. Paydo bo'lganda 'y' ni jo'nating.")

print('Arxivdan chiqarilishi boshlanishi uchun nimadir yozing:')
raw_input(' ')

try:
    os.system("unzip master.zip")
    data = open("./google_appengine/appcfg.py",'r').read()
    if "#!/usr/bin/env python" in data:
        print("\033[4m Google app engine SDK o'rnatildi \033[0m")
    else:
        print("\033[4m Google app engine SDK o'rnatilmadi. Fayllarni tozalang va qayta o'rnatishga harakat qiling.")
except:
    print("\033[4m Google app engine SDK o'rnatilmadi. Fayllar hali tayyor emas")
    
print("Ok, endi @botfather ga kiring va \033[95m/newbot\033[0m buyrug'ini bering. Keyin, bo'tni ismini (nikini) yozing. Undan keyin bo'tni \033[95m @userneym \033[0m ini yozing. Agar boy yasalmasa, unda boshqa userneym bilan harakat qiling. Bo't \033[95m @userneym`i \033[95m ohiri \033[95m bot \033[0m yoki \033[95m _bot \033[0m bilan tugashi kerak.")
p = True
API_TOKEN = ""
while p:
    print("Botfather bergan tokenni yozing")
    for t in raw_input("token:").split("\n"):
        if not(" " in t) and p:
            print(t + "tokenga tekshirilmoqda")
            try:
                data = urllib2.urlopen("https://api.telegram.org/bot"+t+"/getMe").read()
                print("Bo't topildi! Userneym: @"+str(json.loads(data)['result']['username']))
                API_TOKEN = t
                p=False
            except:
                print(t + "tokenga to'g'ri kelmaydi")
    if len(API_TOKEN)>1:
        print("Token topildi.")
    else:
        print("Token topilmadi. Qaytadan hatakat qipko'ring")

print("O'zingizni id raqamingizni yozing. Uni @intelekt_bot ga /id buyrug'ini berib bilsa bo'ladi. Agar noto'g'ri id yozsangiz, unda boshqa odam bo'tga admin bo'lip qoladi")
admin_id = 0
while admin_id == 0:
    try:
        a_id = int(raw_input('id: '))
        admin_id = a_id
    except:
        print("\033[1m id raqam bo'ladi \033[0m")
        


print("Google app engine dagi ochgan projectingizni id sini yozing. Projectingizni nomini yozganingizda tegida chiqishi kerak. Ba'zida project nomi bilan bir xil bo'ladi, ba'zida esa, project nomi dan keyin chiziqcha va raqamlar bo'ladi")
project_id = ""
while project_id == "":
    project_id = raw_input("Proekt id si:")
    l = [' ', "'", '.', ',', '_', '"', "\\", '/', '@']
    for ll in l:
        if ll in project_id:
            project_id = ''
    

print("Fayllar sozlanmoqda...")
data = open('app_engine_installer/app_engine_project/app.yaml','r').read()
data = data.replace('project_nomi', project_id)
open('app_engine_installer/app_engine_project/app.yaml','w').write(data)
data = open('app_engine_installer/app_engine_project/main.py','r').read()
data = data.replace('project_nomi', project_id)
data = data.replace('replace_me_with_token',API_TOKEN)
data = data.replace('8768957689476', str(admin_id))
open('app_engine_installer/app_engine_project/main.py','w').write(data)

print("Ok, ohiriga kelib qoldik. Bo't deyali tayyor. https://appengine.google.com saytiga kiring, yangi ochgan projectingizni tanlang. saytda tepada chap tomonda menyu bor. Menyuga kiring. Usha menyudan \033[95m APP ENGINE \033[0m ni tanlang.\n\nOchilgan stranitsada Choose language yoki Выбрать язык ni bosing. Pasda python ni belgisi chiqib keladi. Ushani tanlang. Karta chiqib kelganda Europe-West (Yevropa) ni tanlang. Pasda next ni bosing. Serverla tayyor bo'lishini kuting. tayyor bo'lganda esa, Tayyor dip yozing.")
while raw_input('//>').lower() != "tayyor":
    print("Yaxshilab e'tibor berip qidiring. Script sizga buni qilib berolmaydi!")
    
print("Agar hammasi tayyor bo'lsa, bo'tni serverga joylimiza. faqat siz avtorizatsiyadan o'tishiz kere. Hozir link chiqadi va siz ucha linkga kirib kod ni copy qilib kelasiz. Keyin terminalga yozasiz. Ok?")
raw_input('>')
os.system('app_engine_installer/google_app_engine/appcfg.py -A '+ project_id + " update app_engine_installer/app_engine_project/app.yaml")

try:
    urllib2.urlopen('https://' + project_id + ".appspot.com/set_webhook").read()
    print("Agar siz hammasini to'g'ri qilgan bo'lsangiz, bo't ishga tushdi. Muammolar bo'lsa, @python_uzga yozing.")
except:
    print("Server ishlamiyopti. Qandaydir hato bo'lgan")
