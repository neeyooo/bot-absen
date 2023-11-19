import os
import asyncio
import sys
import subprocess
from aiogram import Dispatcher, Bot, executor
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from datetime import date, datetime, timedelta
from selenium import webdriver
from pytanggalmerah import TanggalMerah
import time
import aioschedule as schedule
import multiprocessing
from requests import get
import re

try:
    for i in range(10):
        with open(os.devnull, 'w') as DEVNULL:
            try:
                subprocess.check_call(
                    ['ping', '-c', '1', 'google.com'],
                    stdout=DEVNULL,  # suppress output
                    stderr=DEVNULL
                )
            except subprocess.CalledProcessError:  # apabila gagal
                is_up = False
                print('Not connected to Internet!')
                time.sleep(180)
            else:
                is_up = True
                print('Connected to Internet!')
                print()
                break
finally:
    if is_up:
        pass
    else:
        sys.exit()

# region declare
generator = False
libur_is = False
op = webdriver.ChromeOptions()
op.add_argument("--headless")
op.add_argument("--no-sandbox")
hasil_akhir = ""

t = TanggalMerah()
t.set_timezone("Asia/Makassar")

hari = ("Senin", "Selasa", "Rabu", "Kamis", "Jum'at", "Sabtu", "Minggu")
hari_ini = hari[time.localtime()[6]]
sekarang = time.strftime("%H:%M:%S", time.localtime())

BOT_TOKEN = "SECRET"
ADMIN_ID = SECRET
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

hari=["Senin","Selasa","Rabu","Kamis","Jum'at","Sabtu","Minggu"]
matpel=["PAI","PA","PKK","TLJ","AIJ","ASJ","Bahasa Indonesia","Matematika","PPKN","Bahasa Jepang","Bahasa Inggris"]
# endregion

def logging(sender, sender_id, isi_chat):
    if sender_id != ADMIN_ID:
        file_object = open('/root/logging.txt', 'a')
        jamtanggal = datetime.now().strftime("%d-%m-%Y %H:%M:%S ")
        file_object.write("\nPengirim: {} | ID: {} | Isi chat: {} | {}".format(sender, sender_id, isi_chat, jamtanggal))
        file_object.close()
def tele():
    @dp.message_handler(commands='start')  # start
    async def send_message(message: Message):
        isi_chat = message['text']
        sender = message.from_user.username
        sender_id = message.from_user.id
        await message.reply('Hi! Bot ini adalah bot absen personal use. Tidak untuk publik.')
        print("Pengirim: {} | ID: {} | Isi chat: {}".format(sender, sender_id, isi_chat))
        logging(sender, sender_id, isi_chat)

    @dp.message_handler(commands='show_ip')  # show_ip
    async def send_message(message: Message):
        isi_chat = message['text']
        sender = message.from_user.username
        sender_id = message.from_user.id
        if sender_id == ADMIN_ID:
            ip = get('https://api.ipify.org').text
            reply = 'Your IP is: {}'.format(ip)
        else:
            reply = "Only me can use this command. You can't."
        await message.reply(reply)
        print("Pengirim: {} | ID: {} | Isi chat: {}".format(sender, sender_id, isi_chat))
        logging(sender, sender_id, isi_chat)

    @dp.message_handler(commands='libur')  # libur
    async def send_message(message: Message):
        isi_chat = message['text']
        sender = message.from_user.username
        sender_id = message.from_user.id
        if sender_id == ADMIN_ID:
            global libur_is
            if libur_is == True:
                print("Libur = false")
                libur_is = False
                reply = "Berhasil resume BOT sampai absen berikutnya!"
            elif libur_is == False:
                print("Libur = true")
                libur_is = True
                reply = "Berhasil pause BOT sampai absen berikutnya!"
        else:
            reply = "Only me can use this command. You can't."
        await message.reply(reply)
        print("Pengirim: {} | ID: {} | Isi chat: {}".format(sender, sender_id, isi_chat))
        logging(sender, sender_id, isi_chat)

    @dp.message_handler(commands='status')  # status
    async def send_message(message: Message):
        jam = datetime.now().strftime("%H:%M:%S")
        tanggal = date.today().strftime("%d-%m-%Y")
        hari = ("Senin", "Selasa", "Rabu", "Kamis", "Jum'at", "Sabtu", "Minggu")
        hari_ini = hari[time.localtime()[6]]

        printan = '''Status BOT: Running
Version: 3.0 (fix bug in absen generator)

Hari ini: {}
Tanggal: {}
Jam: {}
'''.format(hari_ini, tanggal, jam)

        isi_chat = message['text']
        sender = message.from_user.username
        sender_id = message.from_user.id
        await message.reply(printan)
        print("Pengirim: {} | ID: {} | Isi chat: {}".format(sender, sender_id, isi_chat))
        logging(sender, sender_id, isi_chat)

    @dp.message_handler(commands='howitworks')  # howitworks
    async def send_message(message: Message):
        isi_chat = message['text']
        sender = message.from_user.username
        sender_id = message.from_user.id

        printan1 = '''1. Apabila libur/tanggal merah, BOT akan pause sampai absen berikutnya. Apabila tidak libur maka BOT akan melakukan kerjanya.
2. Apabila BOT gagal melakukan absen, maka BOT akan mengulang 10x selama 6 menit dalam 60 menit. Apabila BOT berhasil melakukan absen maka BOT akan idle menunggu absen selanjutnya.
3. BOT akan mengirim pesan GAGAL/BERHASIL ke developer lewat Telegram.

𝗕𝗮𝗵𝗮𝘀𝗮 𝗣𝗲𝗺𝗽𝗿𝗼𝗴𝗿𝗮𝗺𝗮𝗻: Python
𝗠𝗼𝗱𝘂𝗹𝗲: aiogram, selenium, aioschedule, pytanggalmerah, requests, asyncio
𝗦𝗲𝗿𝘃𝗲𝗿: STB HG680P - Linux Armbian 20.11 bionic
'''

        await message.reply(printan1)
        print("Pengirim: {} | ID: {} | Isi chat: {}".format(sender, sender_id, isi_chat))
        logging(sender, sender_id, isi_chat)
    @dp.message_handler(commands='generator_absen')  # absen
    async def send_message(message: Message):
        sender_id = message.from_user.id
        if sender_id == ADMIN_ID:
            global generator
            if generator == False:
                generator = True
                printan1 = "Paste absen disini..."
            elif generator == True:
                generator = False
                printan1 = "Berhasil di cancel."
        else:
            printan1 = "Only me can use this command. You can't."
        await message.reply(printan1)
    @dp.message_handler(commands='absen')  # absen
    async def send_message(message: Message):
        isi_chat = message['text']
        sender = message.from_user.username
        sender_id = message.from_user.id

        keyboard = InlineKeyboardMarkup(row_width=2)
        button = InlineKeyboardButton('Hari ini', callback_data="harini")
        button1 = InlineKeyboardButton('Berikutnya', callback_data="besok")
        keyboard.row(button)
        keyboard.row(button1)

        await message.reply(text="Silahkan Pilih", reply_markup=keyboard)
        print("Pengirim: {} | ID: {} | Isi chat: {}".format(sender, sender_id, isi_chat))
        logging(sender, sender_id, isi_chat)

    @dp.message_handler()  # anything
    async def send_welcome(message: Message):
        global generator
        isi_chat = message['text']
        sender = message.from_user.username
        sender_id = message.from_user.id
        """
        This handler will be called when user sends `/start` or `/help` command
        """
        if generator == True:
            file_object = open('/root/absen.txt', 'w')
            file_object.write(isi_chat)
            file_object.close()
            await no_absen()
            generator = False
        else:
            print("Pengirim: {} | ID: {} | Isi chat: {}".format(sender, sender_id, isi_chat))
            logging(sender, sender_id, isi_chat)

    @dp.callback_query_handler(text='sudah')
    async def inline_kb_answer_callback_handler(query: CallbackQuery):
        jam = datetime.now().strftime("%H:%M:%S")
        chatid = query.message.chat.id
        messageid = query.message.message_id
        await query.answer()
        await printan("PKK", "BERHASIL", jam, messageid, chatid)

    @dp.callback_query_handler(text='besok')
    async def inline_kb_answer_callback_handler(query: CallbackQuery):
        besok = hari[(datetime.now() + timedelta(days=1)).weekday()]
        hari_ini = hari[time.localtime()[6]]
        sekarang = datetime.now()
        today5pm = sekarang.replace(hour=17, minute=0, second=0)
        besok1 = datetime.strptime(str(datetime.now() + timedelta(days=1)).split()[0]+" 08:00:00","%Y-%m-%d %H:%M:%S")
        besok2 = datetime.strptime(str(datetime.now() + timedelta(days=1)).split()[0],"%Y-%m-%d").strftime("%Y %m %d").split()
        t.set_date(y=besok2[0], m=besok2[1], d=besok2[2])

        chatid = query.message.chat.id
        messageid = query.message.message_id
        await query.answer()
        if hari_ini == "Jum'at" and sekarang > today5pm:
            printan1 = "Besok hari {}, tidak ada absen.".format(besok)
        elif hari_ini == "Sabtu":
            printan1 = "Besok hari {}, tidak ada absen.".format(besok)
        elif t.is_holiday() or libur_is == True:
            if t.is_holiday():
                printan1 = "Besok libur, {}".format((''.join(t.get_event())))
            printan1 = "Besok libur."
        else:
            if besok == "Senin":
                hasil = "{}(Classroom), {}(Manual), {}(Bot)".format(matpel[0], matpel[2], matpel[3])
                hasil1 = "{}, {}, {}".format(matpel[0], matpel[2], matpel[3])
            elif besok == "Selasa":
                hasil = "{}(Whatsapp), {}(Bot), {}(Classroom)".format(matpel[4], matpel[3], matpel[1])
                hasil1 = "{}, {}, {}".format(matpel[4], matpel[3], matpel[1])
            elif besok == "Rabu":
                hasil = "{}(Whatsapp), {}(Whatsapp), {}(Classroom)".format(matpel[4], matpel[5], matpel[6])
                hasil1 = "{}, {}, {}".format(matpel[4], matpel[5], matpel[6])
            elif besok == "Kamis":
                hasil = "{}(Manual, {}(Whatsapp), {}(Bot)".format(matpel[2], matpel[5], matpel[7])
                hasil1 = "{}, {}, {}".format(matpel[2], matpel[5], matpel[7])
            elif besok == "Jum'at":
                hasil = "{}(Bot), {}(Whatsapp)".format(matpel[7], matpel[9])
                hasil1 = "{}, {}, {}, {}".format(matpel[8], matpel[7], matpel[9], matpel[10])
            printan1 = '''Besok hari: {}
Absen: {}
Mata Pelajaran: {}
Countdown: {}
'''.format(besok, hasil, hasil1, str(besok1 - sekarang).split(".")[0])
        await bot.delete_message(message_id=messageid,chat_id=chatid)
        await bot.send_message(text=printan1, chat_id=chatid)

    @dp.callback_query_handler(text='harini')
    async def inline_kb_answer_callback_handler(query: CallbackQuery):
        hari_ini = hari[time.localtime()[6]]

        chatid = query.message.chat.id
        messageid = query.message.message_id
        await query.answer()
        if hari_ini == "Sabtu" or hari_ini == "Minggu" or libur_is == True or t.is_holiday():
            if t.is_holiday():
                printan1 = "Hari ini libur, {}".format((''.join(t.get_event())))
            printan1 = "Hari ini {}, libur.".format(hari_ini)
        else:
            if hari_ini == "Senin":
                hasil = "{}(Classroom), {}(Manual), {}(Bot)".format(matpel[0], matpel[2], matpel[3])
                hasil1 = "{}, {}, {}".format(matpel[0], matpel[2], matpel[3])
            elif hari_ini == "Selasa":
                hasil = "{}(Whatsapp), {}(Bot), {}(Classroom)".format(matpel[4], matpel[3], matpel[1])
                hasil1 = "{}, {}, {}".format(matpel[4], matpel[3], matpel[1])
            elif hari_ini == "Rabu":
                hasil = "{}(Whatsapp), {}(Whatsapp), {}(Classroom)".format(matpel[4], matpel[5], matpel[6])
                hasil1 = "{}, {}, {}".format(matpel[4], matpel[5], matpel[6])
            elif hari_ini == "Kamis":
                hasil = "{}(Manual, {}(Whatsapp), {}(Bot)".format(matpel[2], matpel[5], matpel[7])
                hasil1 = "{}, {}, {}".format(matpel[2], matpel[5], matpel[7])
            elif hari_ini == "Jum'at":
                hasil = "{}(Bot), {}(Whatsapp)".format(matpel[7], matpel[9])
                hasil1 = "{}, {}, {}, {}".format(matpel[8], matpel[7], matpel[9], matpel[10])
            printan1 = '''Hari: {}
Absen: {}
Mata Pelajaran: {}
'''.format(hari_ini, hasil, hasil1)
        await bot.delete_message(message_id=messageid, chat_id=chatid)
        await bot.send_message(text=printan1, chat_id=chatid)
    executor.start_polling(dp, skip_updates=True)

print('Hari ini:', hari_ini)
print('Sekarang jam:', sekarang)
print("")
time.sleep(1)
print("Menunggu absen...")

async def no_absen():
    file1 = open("/root/absen.txt", 'r+')
    Lines = file1.readlines()
    for line in Lines:
        if "Administrasi Infrastruktur Jaringan" in line:
            async def aij():
                def test():
                    global hasil_akhir
                    i = 0
                    try:
                        with open("/root/absen.txt", 'r') as file:
                            Lines = file.readlines()
                            for line in Lines:
                                i += 1
                                l = line.strip()
                                a = re.findall('^\d+', l)
                                if a:
                                    hasil_akhir = str(a).strip("[']")
                                    try:
                                        a = str(a).strip("[']")
                                        b = str(re.findall('^\d+', str(Lines[i + 2]).strip())).strip("[']")
                                        a1 = int(a)
                                        b1 = int(b)
                                        # print("index =", i, ",", a1, "-", b1, "=", b1 - a1)
                                        if b1 - a1 > 1:
                                            aa = str(a1 + 1)
                                            with open("/root/absen.txt", 'w') as f:
                                                printan = "\n{}. Nama Lengkap: \nNISN: \n".format(aa)
                                                Lines.insert(i + 1, printan)
                                                f.writelines(Lines)
                                    except Exception as e:
                                        pass
                    except:
                        file.close()
                    else:
                        file.close()
                        test()
                def test1():
                    global hasil_akhir
                    i = 0
                    sudah = False
                    try:
                        with open("/root/absen.txt", 'r') as file1:
                            Lines = file1.readlines()
                            for line in Lines:
                                i += 1
                                l = line.strip()
                                a = re.findall('^\d+', l)
                                if a:
                                    try:
                                        a = str(a).strip("[']")
                                        a1 = int(a)
                                        if a == '34':
                                            sudah = True
                                            break
                                        if hasil_akhir == a:
                                            aa = str(a1 + 1)
                                            hasil_akhir = str(a1 + 1)
                                            with open("/root/absen.txt", 'w') as f:
                                                if a == '32':
                                                    printan = "{}. Nama Lengkap: Syarif Hermawan\nNISN: 0046464095\n\n".format(
                                                        aa)
                                                else:
                                                    printan = "{}. Nama Lengkap: \nNISN: \n\n".format(aa)
                                                Lines.insert(i + 2, printan)
                                                f.writelines(Lines)
                                                f.close()
                                            break
                                    except Exception as e:
                                        print(e)
                    except:
                        pass
                    else:
                        if sudah == False:
                            test1()
                        else:
                            pass
                def test2():
                    i = 0
                    with open("/root/absen.txt", 'r') as file1:
                        Lines = file1.readlines()
                        for line in Lines:
                            i += 1
                            l = line.strip()
                            a = re.findall('^33+', l)
                            if a:
                                Lines[i - 1] = "33. Nama Lengkap: Syarif Hermawan\n"
                                Lines[i] = "NISN: 0046464095\n"
                                with open('/root/absen.txt', 'w') as file:
                                    file.writelines(Lines)
                test()
                test1()
                test2()
            await aij()
            break
        if "Jepang" in line:
            async def bjep():
                def test():
                    i = 0
                    global hasil_akhir
                    with open("/root/absen.txt", 'r') as file:
                        Lines = file.readlines()
                        for line in Lines:
                            i += 1
                            l = line.strip()
                            a = re.findall('^\d+', l)
                            if a:
                                hasil_akhir = str(a).strip("[']")
                                try:
                                    a = str(a).strip("[']")
                                    b = str(re.findall('^\d+', str(Lines[i]).strip())).strip("[']")
                                    a1 = int(a)
                                    b1 = int(b)
                                    # print("index =", i, ",", a1, "-", b1, "=", b1 - a1)
                                    if b1 - a1 > 1:
                                        aa = str(a1 + 1)
                                        with open("/root/absen.txt", 'w') as f:
                                            printan = "{}. \n".format(aa)
                                            Lines.insert(i, printan)
                                            f.writelines(Lines)
                                            f.close()
                                            file.seek(0)
                                            continue
                                except IndexError as e:
                                    test1()
                def test1():
                    i = 0
                    global hasil_akhir
                    sudah = False
                    try:
                        with open("/root/absen.txt", 'r') as file:
                            Lines = file.readlines()
                            for line in Lines:
                                i += 1
                                l = line.strip()
                                a = re.findall('^\d+', l)
                                if a:
                                    try:
                                        a = str(a).strip("[']")
                                        a1 = int(a)
                                        if a == '34':
                                            sudah = True
                                            break
                                        if hasil_akhir == a:
                                            aa = str(a1 + 1)
                                            hasil_akhir = str(a1 + 1)
                                            with open("/root/absen.txt", 'w') as f:
                                                if a == '32':
                                                    printan = "\n{}. Syarif Hermawan".format(aa)
                                                else:
                                                    printan = "\n{}. ".format(aa)
                                                Lines.insert(i, printan)
                                                f.writelines(Lines)
                                                f.close()
                                            break
                                    except Exception as e:
                                        print(e)
                    except:
                        pass
                    else:
                        if sudah == False:
                            test1()
                        else:
                            pass
                def test2():
                    i = 0
                    with open("/root/absen.txt", 'r') as file1:
                        Lines = file1.readlines()
                        for line in Lines:
                            i += 1
                            l = line.strip()
                            a = re.findall('^33+', l)
                            if a:
                                Lines[i - 1] = "33. Syarif Hermawan\n"
                                with open('/root/absen.txt', 'w') as file:
                                    file.writelines(Lines)
                test()
                test2()
            await bjep()
            break
    file2 = open("/root/absen.txt", 'r+')
    printan1 = file2.read()
    file2.close()
    await bot.send_message(SECRET,printan1)
async def printan(matpel, kondisi, jam, messageid, chatid):
    tanggal = date.today().strftime("%d-%m-%Y")
    hari_ini = hari[time.localtime()[6]]
    print("Absen {} {}".format(matpel, kondisi))
    print("Mengirim pesan ke Telegram")
    if kondisi == "BERHASIL":
        printan1 = '''𝗛𝗮𝗹𝗼 𝗯𝗮𝗻𝗴 𝗷𝗮𝗴𝗼, ni0
-----------------------------
𝗔𝗕𝗦𝗘𝗡 {} ✅
-----------------------------
Hari: {}
Tanggal: {}
Jam: {}
'''.format(matpel, hari_ini, tanggal, jam)
    if kondisi == "GAGAL":
        printan1 = '''𝗛𝗮𝗹𝗼 𝗯𝗮𝗻𝗴 𝗷𝗮𝗴𝗼, ni0
-----------------------------
𝗔𝗕𝗦𝗘𝗡 {} ❌
-----------------------------
Hari: {}
Tanggal: {}
Jam: {}
'''.format(matpel, hari_ini, tanggal, jam)
    if matpel == "PKK":
        await bot.edit_message_text(text=printan1, message_id=messageid, chat_id=chatid)
    else:
        await bot.send_message(SECRET, printan1)
async def print_libur(kondisi):
    global libur_is
    print("")
    tanggal = date.today().strftime("%d-%m-%Y")
    hari_ini = hari[time.localtime()[6]]
    if kondisi == "tglmerah":
        printan = '''𝗛𝗮𝗹𝗼 𝗯𝗮𝗻𝗴 𝗷𝗮𝗴𝗼, ni0
-----------------------------
BOT dipause dikarenakan libur!
-----------------------------
Hari: {}
Tanggal: {}
Deskripsi: {}
'''.format(hari_ini, tanggal, (''.join(t.get_event())))
    if kondisi == "libur":
        printan = '''𝗛𝗮𝗹𝗼 𝗯𝗮𝗻𝗴 𝗷𝗮𝗴𝗼, ni0
-----------------------------
BOT dipause dikarenakan libur!
-----------------------------
Hari: {}
Tanggal: {}
'''.format(hari_ini, tanggal)
        libur_is = False
    print("BOT dipause dikarenakan libur")
    print("")
    await bot.send_message(SECRET, printan)

async def pkk():
    print("Memberikan absen PKK")
    print("")
    keyboard = InlineKeyboardMarkup(row_width=2)
    button = InlineKeyboardButton('Link',
                                  url='https://forms.zohopublic.com/omjusgen/form/DaftarHadirXTKJ4/formperma/vpLUgmoQDh3PUVbZ6OQK01wgIZSMt2cxBN4U7CCTZHk')
    button1 = InlineKeyboardButton('Selesai', callback_data="sudah")
    keyboard.row(button)
    keyboard.row(button1)
    await bot.send_message(SECRET,
                           "Silahkan absen PKK secara manual melalui link dibawah ini. Dan apabila sudah klik tombol Selesai.",
                           reply_markup=keyboard)
async def senin():
    global libur_is
    async def tlj_senin():
        for i in range(10):
            try:
                # region TLJ_senin
                today = date.today().strftime("%d-%m-%Y")
                print("Mencoba absen TLJ")
                a = webdriver.Chrome(options=op)
                ###Masuk Web####
                a.get(
                    'SECRET')  # Masuk web
                time.sleep(2)
                ###Nama###
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[1]/div[1]').click()
                time.sleep(2)
                options = a.find_elements_by_xpath("//*[contains(text(), 'SYARIF HERMAWAN')]")
                options[1].click()  # Mengklik index ke 1, 1=SYARIF HERMAWAN
                time.sleep(2)
                ###Pilih Kelas###
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div[1]/div[1]').click()
                time.sleep(2)
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[3]').click()
                time.sleep(2)
                ###Tulis Nama###
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]').click()
                time.sleep(2)
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[2]/div[3]').click()
                time.sleep(2)
                ###Submit Button###
                a.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div/div[1]/div/span').click()
                time.sleep(2)
                # endregion
            except:
                jam = datetime.now().strftime("%H:%M:%S")
                await printan("TLJ", "GAGAL", jam, "", "")
                time.sleep(2)
                a.__exit__()
                print("Mencoba ulang bot dalam 360 detik, selama 10x")
                print("")
                time.sleep(360)
            else:
                jam = datetime.now().strftime("%H:%M:%S")
                await printan("TLJ", "BERHASIL", jam, "", "")
                time.sleep(2)
                a.__exit__()
                print("")
                break
    if libur_is == False:
        print("")
        if t.is_holiday():
            await print_libur("tglmerah")
        else:
            await tlj_senin()
            await pkk()
    if libur_is == True:
        await print_libur("libur")
async def selasa():
    global libur_is
    async def tlj_selasa():
        for i in range(10):
            try:
                # region TLJ_selasa
                today = date.today().strftime("%d-%m-%Y")
                print("Mencoba absen TLJ")
                a = webdriver.Chrome(options=op)
                ###Masuk Web####
                a.get(
                    'SECRET')  # Masuk web
                time.sleep(2)
                ###Nama###
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[1]/div[1]').click()
                time.sleep(2)
                options = a.find_elements_by_xpath("//*[contains(text(), 'SYARIF HERMAWAN')]")
                options[1].click()  # Mengklik index ke 1, 1=SYARIF HERMAWAN
                time.sleep(2)
                ###Pilih Kelas###
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div[1]/div[1]').click()
                time.sleep(2)
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[3]').click()
                time.sleep(2)
                ###Tulis Nama###
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]').click()
                time.sleep(2)
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[2]/div[3]').click()
                time.sleep(2)
                ###Submit Button###
                a.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div/div[1]/div/span').click()
                time.sleep(2)
                # endregion
            except:
                jam = datetime.now().strftime("%H:%M:%S")
                await printan("TLJ", "GAGAL", jam, "", "")
                time.sleep(2)
                a.__exit__()
                print("Mencoba ulang bot dalam 360 detik, selama 10x")
                print("")
                time.sleep(360)
            else:
                jam = datetime.now().strftime("%H:%M:%S")
                await printan("TLJ", "BERHASIL", jam, "", "")
                time.sleep(2)
                a.__exit__()
                print("")
                break
    if libur_is == False:
        print("")
        if t.is_holiday():
            await print_libur("tglmerah")
        else:
            await tlj_selasa()
    if libur_is == True:
        await print_libur("libur")
async def kamis():
    global libur_is
    async def mtk_kamis():
        for i in range(10):
            try:
                # region MTK_kamis
                today = date.today().strftime("%d-%m-%Y")
                print("Mencoba absen MTK")
                a = webdriver.Chrome(options=op)
                ###Masuk Web####
                a.get(
                    'SECRET')  # Masuk web
                time.sleep(2)
                ###Tanggal###
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input').send_keys(
                    today)
                time.sleep(2)
                ###Isi absensi###
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div[1]/div[1]').click()
                time.sleep(2)
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[3]').click()
                time.sleep(2)
                ###Pilih Kelas###
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]').click()
                time.sleep(2)
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[2]/div[8]').click()
                time.sleep(2)
                ###Berikutnya###
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[3]/div/div[1]/div/span').click()
                time.sleep(10)
                ###Pilih nama###
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div[1]/div[1]').click()
                time.sleep(2)
                options = a.find_elements_by_xpath("//*[contains(text(), 'SYARIF HERMAWAN')]")
                options[1].click()  # Mengklik index ke 1, 1=SYARIF HERMAWAN
                time.sleep(2)
                ###Submit Button###
                a.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div/div[1]/div[2]/span').click()
                time.sleep(2)
                # endregion
            except:
                jam = datetime.now().strftime("%H:%M:%S")
                await printan("Matematika", "GAGAL", jam, "", "")
                time.sleep(2)
                a.__exit__()
                print("Mencoba ulang bot dalam 360 detik, selama 10x")
                print("")
                time.sleep(360)
            else:
                jam = datetime.now().strftime("%H:%M:%S")
                await printan("Matematika", "BERHASIL", jam, "", "")
                time.sleep(2)
                a.__exit__()
                print("")
                break
    if libur_is == False:
        print("")
        if t.is_holiday():
            await print_libur("tglmerah")
        else:
            await mtk_kamis()
            await pkk()
    if libur_is == True:
        await print_libur("libur")
async def jumat():
    global libur_is
    async def mtk_Jumat():
        for i in range(10):
            try:
                # region MTK_Jumat
                today = date.today().strftime("%d-%m-%Y")
                print("Mencoba absen MTK")
                a = webdriver.Chrome(options=op)
                ###Masuk Web####
                a.get(
                    'SECRET')  # Masuk web
                time.sleep(2)
                ###Tanggal###
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input').send_keys(
                    today)
                time.sleep(2)
                ###Isi absensi###
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div[1]/div[1]').click()
                time.sleep(2)
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[3]').click()
                time.sleep(2)
                ###Pilih Kelas###
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]').click()
                time.sleep(2)
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[2]/div[8]').click()
                time.sleep(2)
                ###Berikutnya###
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[3]/div/div[1]/div/span').click()
                time.sleep(10)
                ###Pilih nama###
                a.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div[1]/div[1]').click()
                time.sleep(2)
                options = a.find_elements_by_xpath("//*[contains(text(), 'SYARIF HERMAWAN')]")
                options[1].click()  # Mengklik index ke 1, 1=SYARIF HERMAWAN
                time.sleep(2)
                ###Submit Button###
                a.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div/div[1]/div[2]/span').click()
                time.sleep(2)
                # endregion
            except:
                jam = datetime.now().strftime("%H:%M:%S")
                await printan("Matematika", "GAGAL", jam, "", "")
                time.sleep(2)
                a.__exit__()
                print("Mencoba ulang bot dalam 360 detik, selama 10x")
                print("")
                time.sleep(360)
            else:
                jam = datetime.now().strftime("%H:%M:%S")
                await printan("Matematika", "BERHASIL", jam, "", "")
                time.sleep(2)
                a.__exit__()
                print("")
                break
    if libur_is == False:
        print("")
        if t.is_holiday():
            await print_libur("tglmerah")
        else:
            await mtk_Jumat()
    if libur_is == True:
        await print_libur("libur")
def scheduler():
    schedule.every().monday.at("08:00").do(senin)
    schedule.every().tuesday.at("08:00").do(selasa)
    schedule.every().thursday.at("08:00").do(kamis)
    schedule.every().friday.at("08:00").do(jumat)
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete(schedule.run_pending())
        time.sleep(0.1)

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=tele)
    p2 = multiprocessing.Process(target=scheduler)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
