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

from telethon import events, Button
from ethon.teleutils import mention
from ethon.mystarts import vc_menu

from .. import MSDZULQURNAIN, ACCESS_CHANNEL, AUTH_USERS

from main.plugins.actions import set_thumbnail, rem_thumbnail, heroku_restart
from LOCAL.localisation import START_TEXT as mulai
from LOCAL.localisation import donate_text, join_text, thumbnail_text, info_text, spam_notice, help_text, source_text, SUPPORT_LINK

@MSDZULQURNAIN.on(events.NewMessage(incoming=True, pattern="/start"))
async def start(event):
    await event.reply(f'{mulai}', 
                      buttons=[[
                               Button.url("DEVELOPER👤", url="https://t.me/MSDZULQURNAIN")],
                               [
                               Button.url("🄼🅂 ק𝙍♢JΞC†", url="https://t.me/MSPR0JECT"),
                               Button.url("🄼🅂 Ꮥᴜקק♢ꭈׁׅ†", url="https://t.me/MsSUPP0RT")],
                               [
                               Button.inline("TENTANG SAYA💻", data="tentang")
                              ]])
    tag = f'[{event.sender.first_name}](tg://user?id={event.sender_id})'
    await MSDZULQURNAIN.send_message(int(ACCESS_CHANNEL), f'{tag} MEMULAI BOT✔\n\nID : `{zid}`')
    zid = f'{event.sender_id}'

@MSDZULQURNAIN.on(events.NewMessage(incoming=True, pattern="/help"))
async def help(event):
    await event.reply(f'{help_text}',
                           buttons=[[
                                    Button.inline("DONATE🙏", data="donasi")],
                                    [
                                    Button.inline("TUTUP🚪", data="tutup")
                                   ]]) 
    
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="donasi"))
async def tutup(event):  
    await event.reply(f'{donate_text}')
    
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="tentang"))
async def tentang(event):  
    await event.reply(f'{info_text}')
    
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="tutup"))
async def tutup(event):  
    await event.delete()
    
@MSDZULQURNAIN.on(events.NewMessage(incoming=True, pattern="/thumbnail"))
async def thumbnail(event):
    await event.reply(f'**RULES MEMASANG THUMBNAIL😒**\n\n{thumbnail_text}',
                      buttons=[[
                                Button.inline("PASANG THUMBNAIL🖼", data="sett")],
                                [
                                Button.inline("HAPUS THUMBNAIL🗑", data="remt")],
                                [
                                Button.inline("TUTUP🚪", data="tutup")
                              ]])
                         
                    
@MSDZULQURNAIN.on(events.NewMessage(incoming=True, pattern="/join"))
async def join(event):
    await event.reply(f'{join_text}', 
                      buttons=[[
                                Button.url("🄹♢ɨ𝐍  🄲ΉΛ𝐍𝐍ΞꝈ", url="https://t.me/MsSUPP0RT")], 
                                [
                                Button.url("🄹♢ɨ𝐍  🄲ΉΛ𝐍𝐍ΞꝈ", url="https://shareduit.pw/B26BYC4zT")],
                                [Button.inline("TUTUP🚪", data="tutup")
                              ]]) 
    

                   
 #-----------------------------------------------------------------------------------------------                            
    
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="sett"))
async def sett(event):    
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    async with MSDZULQURNAIN.conversation(event.chat_id) as conv: 
        xx = await conv.send_message("Kirim saya foto untuk thumbnail dengan reply pesan ini")
        x = await conv.get_reply()
        if not x.media:
            xx.edit("Media tidak ada")
        mime = x.file.mime_type
        if not 'png' in mime:
            if not 'jpg' in mime:
                if not 'jpeg' in mime:
                    return await xx.edit("Foto tidak ada")
        await set_thumbnail(event, x.media)
        await xx.delete()
        
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="remt"))
async def remt(event):  
    await event.delete()
    await rem_thumbnail(event)

@MSDZULQURNAIN.on(events.NewMessage(incoming=True, pattern="/restart"))
async def restart(event):
    await event.reply(f'{restart}')
    
@MSDZULQURNAIN.on(events.callbackquery.CallbackQuery(data="restart"))
async def res(event):
    if not f'{event.sender_id}' == f'{int(AUTH_USERS)}':
        return await event.edit("Hanya admin yg dapat merestart")
    result = await heroku_restart()
    if result is None:
        await event.edit("Kamu belum mengisi `HEROKU_API` dan `HEROKU_APP_NAME` vars.")
    elif result is False:
        await event.edit("Terjadi kesalahan🗿")
    elif result is True:
        await event.edit("Sedang merestart app, tunggu beberapa menit")
