#  This file is part of the VIDEOconvertor distribution.
#  Copyright (c) 2021 vasusen-code ; All rights reserved. 
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#
#  License can be found in < https://github.com/vasusen-code/VIDEOconvertor/blob/public/LICENSE> .

import os, time, asyncio

from telethon import events, Button
from telethon.tl.types import DocumentAttributeVideo
from ethon.telefunc import fast_download
from ethon.pyfunc import video_metadata

from .. import MSDZULQURNAIN, LOG_CHANNEL, FORCESUB_UN, MONGODB_URI, ACCESS_CHANNEL

from main.plugins.rename import media_rename
from main.plugins.trimmer import trim
from main.plugins.convertor import mp3, flac, wav, mp4, mkv, webm, file, video
from main.Database.database import Database
from main.plugins.actions import force_sub
from main.plugins.ssgen import screenshot
from LOCAL.localisation import source_text, SUPPORT_LINK

#Don't be a MF by stealing someone's hardwork.
forcesubtext = f"❌❌❌\n\nIni tidak akan berfungsi,silahkan ketik `/join` dan join semua channel sebelum menggunakan saya😏"
                
@MSDZULQURNAIN.on(events.NewMessage(incoming=True,func=lambda e: e.is_private))
async def compin(event):
    db = Database(MONGODB_URI, 'videoconvertor')
    if event.is_private:
        media = event.media
        if media:
            yy = await force_sub(event.sender_id)
            if yy is True:
                return await event.reply(forcesubtext)
            banned = await db.is_banned(event.sender_id)
            if banned is True:
                return await event.reply(f'Kamu telah dibanned!\n\ncontact [SUPPORT]({SUPPORT_LINK})', link_preview=False)
            video = event.file.mime_type
            if 'video' in video:
                await event.reply("**MS VIDEO EDITOR📽🎞**\n\nBot hanya bisa di akses 1 pengguna di 1 waktu,Jika kamu spam maka akan otomatis **KEBANNED**😏",
                            buttons=[
                                [Button.inline("EXTRACT AUDIO MP3🎼", data="extaudio")],
                                [Button.inline("CONVERT FORMAT🔀", data="convert")],
                                [Button.inline("UBAH NAMA📝", data="rename")],
                                [Button.inline("SCREENSHOT📸", data="sshots")],
                                [Button.inline("POTONG DURASI✂", data="trim")]
                            ])
            elif 'png' in video:
                return
            elif 'jpeg' in video:
                return
            elif 'jpg' in video:
                return    
            else:
                await event.reply('📦',
                            buttons=[  
                                [Button.inline("UBAH NAMA📝", data="rename")]])
    await event.forward_to(int(ACCESS_CHANNEL))
    

     
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="extaudio"))
async def _compress(event):
    await event.edit("**EXTRACT VIDEO MU MENJADI AUDIO MP3**😊",
                    buttons=[
                        [Button.inline("EXTRACT", data="mp3")],
                        [Button.inline("KEMBALI", data="back")]])

@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="convert"))
async def convert(event):
    button = await event.get_message()
    msg = await button.get_reply_message()  
    await event.edit("**CONVERT FORMAT**🔀",
                    buttons=[
                        [Button.inline("FLAC", data="flac"),
                         Button.inline("WAV", data="wav")],
                        [Button.inline("MP4", data="mp4"),
                         Button.inline("WEBM", data="webm"),
                         Button.inline("MKV", data="mkv")],
                        [Button.inline("FILE", data="file"),
                         Button.inline("VIDEO", data="video")],
                        [Button.inline("KEMBALI", data="back")]])
                        
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="back"))
async def back(event):
    await event.edit("**MS VIDEO EDITOR📽🎞**\n\nBot hanya bisa di akses 1 pengguna di 1 waktu,Jika kamu spam maka akan otomatis **KEBANNED**😏",
                       buttons=[
                                [Button.inline("EXTRACT AUDIO MP3🎼", data="extaudio")],
                                [Button.inline("CONVERT FORMAT🔀", data="convert")],
                                [Button.inline("UBAH NAMA📝", data="rename")],
                                [Button.inline("SCREENSHOT📸", data="sshots")],
                                [Button.inline("POTONG DURASI✂", data="trim")]
                               ])
    
#-----------------------------------------------------------------------------------------

process1 = []
timer = []

#Set timer to avoid spam
async def set_timer(event, list1, list2):
    now = time.time()
    list2.append(f'{now}')
    list1.append(f'{event.sender_id}')
    await event.client.send_message(event.chat_id, 'Kamu bisa mengedit lagi setelah 5 menit🤣')
    await asyncio.sleep(300)
    list2.pop(int(timer.index(f'{now}')))
    list1.pop(int(process1.index(f'{event.sender_id}')))
    
#check time left in timer
async def check_timer(event, list1, list2):
    if f'{event.sender_id}' in list1:
        index = list1.index(f'{event.sender_id}')
        last = list2[int(index)]
        present = time.time()
        return False, f"Tunggu {300-round(present-float(last))} detik untuk mengedit lagi🙃"
    else:
        return True, None
    
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="mp3"))
async def vtmp3(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    if not os.path.isdir("audioconvert"):
        await event.delete()
        os.mkdir("audioconvert")
        await mp3(event, msg)
        os.rmdir("audioconvert")
    else:
        await event.edit("Bot sedang mengedit video pengguna lain, tunggu sampai proses lain selesai!😼")
        
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="flac"))
async def vtflac(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("audioconvert"):
        await event.delete()
        os.mkdir("audioconvert")
        await flac(event, msg)
        os.rmdir("audioconvert")
    else:
        await event.edit("Bot sedang mengedit video pengguna lain, tunggu sampai proses lain selesai!😼")
        
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="wav"))
async def vtwav(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    if not os.path.isdir("audioconvert"):
        await event.delete()
        os.mkdir("audioconvert")
        await wav(event, msg)
        os.rmdir("audioconvert")
    else:
        await event.edit("Bot sedang mengedit video pengguna lain, tunggu sampai proses lain selesai!😼")
        
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="mp4"))
async def vtmp4(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await mp4(event, msg)
    
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="mkv"))
async def vtmkv(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await mkv(event, msg)  
    
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="webm"))
async def vtwebm(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await webm(event, msg)  
    
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="file"))
async def vtfile(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await file(event, msg)    

@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="video"))
async def ftvideo(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await video(event, msg)
    
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="rename"))
async def rename(event):    
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    await event.delete()
    markup = event.client.build_reply_markup(Button.force_reply())
    async with MSDZULQURNAIN.conversation(event.chat_id) as conv: 
        cm = await conv.send_message("Kirim saya nama baru untuk file dengan reply pesan ini!\n\n**CONTOH:** kamu nanyaa,kamu bertanya tanya🗿", buttons=markup)                              
        try:
            m = await conv.get_reply()
            new_name = m.text
            await cm.delete()                    
            if not m:                
                return await cm.edit("Respon tidak tersedia")
        except Exception as e: 
            print(e)
            return await cm.edit("Terjadi kesalahan saat menunggu respons")
    await media_rename(event, msg, new_name)  
    
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="fcomp"))
async def fcomp(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    if f'{event.sender_id}' in process1:
        index = process1.index(f'{event.sender_id}')
        last = timer[int(index)]
        present = time.time()
        return await event.answer(f"Tunggu {300-round(present-float(last))} detik untuk mengedit lagi🙃", alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await compress(event, msg, ffmpeg_cmd=2)
        os.rmdir("encodemedia")
        now = time.time()
        timer.append(f'{now}')
        process1.append(f'{event.sender_id}')
        await event.client.send_message(event.chat_id, 'Kamu bisa mengedit lagi setelah 5 menit🤣')
        await asyncio.sleep(300)
        timer.pop(int(timer.index(f'{now}')))
        process1.pop(int(process1.index(f'{event.sender_id}')))
    else:
        await event.edit(f"Bot sedang mengedit video pengguna lain, tunggu sampai proses lain selesai!😼\n\n**[LOG CHANNEL](https://t.me/{LOG_CHANNEL})**", link_preview=False)
                       
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="hcomp"))
async def hcomp(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    if f'{event.sender_id}' in process1:
        index = process1.index(f'{event.sender_id}')
        last = timer[int(index)]
        present = time.time()
        return await event.answer(f"Tunggu {300-round(present-float(last))} detik untuk mengedit lagi🙃", alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await compress(event, msg, ffmpeg_cmd=1)
        os.rmdir("encodemedia")
        now = time.time()
        timer.append(f'{now}')
        process1.append(f'{event.sender_id}')
        await event.client.send_message(event.chat_id, 'Kamu bisa mengedit lagi setelah 5 menit🤣')
        await asyncio.sleep(300)
        timer.pop(int(timer.index(f'{now}')))
        process1.pop(int(process1.index(f'{event.sender_id}')))
    else:
        await event.edit(f"Bot sedang mengedit video pengguna lain, tunggu sampai proses lain selesai!😼\n\n**[LOG CHANNEL](https://t.me/{LOG_CHANNEL})**", link_preview=False)

@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="264"))
async def _264(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await compress(event, msg, ffmpeg_cmd=4, ps_name="**ENCODING:**")
        os.rmdir("encodemedia")
        await set_timer(event, process1, timer) 
    else:
        await event.edit(f"Bot sedang mengedit video pengguna lain, tunggu sampai proses lain selesai!😼\n\n**[LOG CHANNEL](https://t.me/{LOG_CHANNEL})**", link_preview=False)
      
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="265"))
async def _265(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await compress(event, msg, ffmpeg_cmd=3, ps_name="**ENCODING:**")
        os.rmdir("encodemedia")
        await set_timer(event, process1, timer) 
    else:
        await event.edit(f"Bot sedang mengedit video pengguna lain, tunggu sampai proses lain selesai!😼\n\n**[LOG CHANNEL](https://t.me/{LOG_CHANNEL})**", link_preview=False)
        
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="240"))
async def _240(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await encode(event, msg, scale=240)
        os.rmdir("encodemedia")
        await set_timer(event, process1, timer) 
    else:
        await event.edit(f"Bot sedang mengedit video pengguna lain, tunggu sampai proses lain selesai!😼\n\n**[LOG CHANNEL](https://t.me/{LOG_CHANNEL})**", link_preview=False)
        
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="360"))
async def _360(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await encode(event, msg, scale=360)
        os.rmdir("encodemedia")
        await set_timer(event, process1, timer) 
    else:
        await event.edit(f"Bot sedang mengedit video pengguna lain, tunggu sampai proses lain selesai!😼\n\n**[LOG CHANNEL](https://t.me/{LOG_CHANNEL})**", link_preview=False)
        
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="480"))
async def _480(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await encode(event, msg, scale=480)
        os.rmdir("encodemedia")
        await set_timer(event, process1, timer) 
    else:
        await event.edit(f"Bot sedang mengedit video pengguna lain, tunggu sampai proses lain selesai!😼\n\n**[LOG CHANNEL](https://t.me/{LOG_CHANNEL})**", link_preview=False)
        
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="720"))
async def _720(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    s, t = await check_timer(event, process1, timer) 
    if s == False:
        return await event.answer(t, alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await encode(event, msg, scale=720)
        os.rmdir("encodemedia")
        await set_timer(event, process1, timer) 
    else:
        await event.edit(f"Bot sedang mengedit video pengguna lain, tunggu sampai proses lain selesai!😼\n\n**[LOG CHANNEL](https://t.me/{LOG_CHANNEL})**", link_preview=False)
          
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="sshots"))
async def ss_(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    if f'{event.sender_id}' in process1:
        index = process1.index(f'{event.sender_id}')
        last = timer[int(index)]
        present = time.time()
        return await event.answer(f"Tunggu {120-round(present-float(last))} detik untuk mengedit lagi 🙃", alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()
    await event.delete()
    await screenshot(event, msg)    
    now = time.time()
    timer.append(f'{now}')
    process1.append(f'{event.sender_id}')
    await event.client.send_message(event.chat_id, 'Kamu bisa mengedit lagi setelah 2 menit🤗')
    await asyncio.sleep(120)
    timer.pop(int(timer.index(f'{now}')))
    process1.pop(int(process1.index(f'{event.sender_id}')))
    
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="trim"))
async def vtrim(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    await event.delete()
    markup = event.client.build_reply_markup(Button.force_reply())
    async with MSDZULQURNAIN.conversation(event.chat_id) as conv: 
        try:
            xx = await conv.send_message("Kirim saya jam/menit/detik PERTAMA dengan reply pesan ini. \n\n**Dalam format jam:menit:detik**\n\nCONTOH DURASI JAM: `01:00:00`\nCONTOH DURASI MENIT: `00:01:00`\nCONTOH DURASI DETIK: `00:00:10` ", buttons=markup)
            x = await conv.get_reply()
            st = x.text
            await xx.delete()                    
            if not st:               
                return await xx.edit("Respon tidak tersedia")
        except Exception as e: 
            print(e)
            return await xx.edit("Terjadi kesalahan saat menunggu respons")
        try:
            xy = await conv.send_message("Kirim saya jam/menit/detik TERAKHIR dengan reply pesan ini.  \n\n**Dalam format jam:menit:detik**\n\nCONTOH DURASI JAM: `03:00:00`\nCONTOH DURASI MENIT: `00:05:00`\nCONTOH DURASI DETIK: `00:00:30` ", buttons=markup)
            y = await conv.get_reply()
            et = y.text
            await xy.delete()                    
            if not et:                
                return await xy.edit("Respon tidak tersedia")
        except Exception as e: 
            print(e)
            return await xy.edit("Terjadi kesalahan saat menunggu respons")
        await trim(event, msg, st, et)
