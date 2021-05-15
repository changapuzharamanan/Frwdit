#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Dark Angel

import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait
from config import Config
from translation import Translation
import os 
import sys
from user import User
FROM = Config.FROM_CHANNEL
TO = Config.TO_CHANNEL
FILTER = Config.FILTER_TYPE

@Client.on_message(filters.command("stop"))
async def stop_button(bot, message):
    if str(message.from_user.id) not in Config.OWNER_ID:
        return
    msg = await bot.send_message(
        text="<i>Trying To Stoping.....</i>",
        chat_id=message.chat.id
    )
    await asyncio.sleep(5)
    await msg.edit("<i>File Forword Stoped Successfully 👍</i>")
    os.execl(sys.executable, sys.executable, *sys.argv)
    
 
@Client.on_message(filters.private & filters.command(["run"]))
async def run(bot, message):
    if str(message.from_user.id) not in Config.OWNER_ID:
        return
    buttons = [[
        InlineKeyboardButton('🚫 STOP', callback_data='stop_btn')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    m = await bot.send_message(
        text="<i>File Forwording Started😉</i>",
        reply_markup=reply_markup,
        chat_id=message.chat.id
    )

    files_count = 0
    async for message in bot.USER.search_messages(chat_id=FROM,offset=Config.SKIP_NO,limit=Config.LIMIT,filter=FILTER):
        try:
            if message.video:
                file_name = message.video.file_name
                file_id = message.video.file_id
            elif message.document:
                file_name = message.document.file_name
                file_id = message.document.file_id
            elif message.audio:
                file_name = message.audio.file_name
                file_id = message.audio.file_id
            else:
                file_id = None
                file_name = None
            message = await bot.get_messages(FROM, message.message_id)
            await bot.send_cached_media(TO, file_id)
            files_count += 1
            await asyncio.sleep(1)
            new_skip_NO=str(int(Config.SKIP_NO)+int(files_count))
            print(f"Total Forwarded : {files_count}\nNow Forwarded: {file_name}\nCurrent SKIP_NO: {new_skip_NO}") 
            try:
                await m.edit(text=f"Total Forwarded : <code>{files_count}</code>\nCurrent SKIP_NO:<code>{new_skip_NO}</code>\nNow Forwarded: <code>{file_name}</code>")
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except Exception as e:
                print(e)
                pass
                             
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            print(e)
            pass
   # await m.delete()
    buttons = [[
        InlineKeyboardButton('📜 Support Group', url='https://t.me/DxHelpDesk')
    ]] 
    reply_markup = InlineKeyboardMarkup(buttons)
    await m.edit(
        text=f"<u><i>Successfully Forwarded</i></u>\n\n<b>Total Forwarded Files:-</b> <code>{files_count}</code> <b>Files</b>\n<b>Thanks For Using Me❤️</b>",
        reply_markup=reply_markup
    )
        

