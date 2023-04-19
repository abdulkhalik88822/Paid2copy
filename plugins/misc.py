import os
import asyncio
from utils import *
from info import *
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from pyrogram.types import Message, User, ChatJoinRequest

@Client.on_message(filters.command("start") & ~filters.channel)
async def start(bot, message):
    await add_user(message.from_user.id, message.from_user.first_name)
    await message.reply(text=script.START.format(message.from_user.mention),
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕', url=f'http://t.me/yourresultsrobot?startgroup=true')
            ],[InlineKeyboardButton("ʜᴇʟᴘ", callback_data="misc_help"),
                                                            InlineKeyboardButton("Donate_us", callback_data="misc_buymoney")]]))  
@Client.on_message(filters.command("help"))
async def help(bot, message):
    await message.reply(text=script.HELP, 
                        disable_web_page_preview=True)

@Client.on_message(filters.command("stats") & filters.user(ADMIN))
async def stats(bot, message):
    g_count, g_list = await get_groups()
    u_count, u_list = await get_users()
    await message.reply(script.STATS.format(u_count, g_count))

@Client.on_message(filters.command("id"))
async def id(bot, message):
    text = f"Current Chat ID: `{message.chat.id}`\n"
    if message.from_user:
       text += f"Your ID: `{message.from_user.id}`\n"
    if message.reply_to_message:
       if message.reply_to_message.from_user:
          text += f"Replied User ID: `{message.reply_to_message.from_user.id}`\n"
       if message.reply_to_message.forward_from:
          text += f"Replied Message Forward from User ID: `{message.reply_to_message.forward_from.id}`\n"
       if message.reply_to_message.forward_from_chat:
          text += f"Replied Message Forward from Chat ID: `{message.reply_to_message.forward_from_chat.id}\n`"
    await message.reply(text)

@Client.on_callback_query(filters.regex(r"^misc"))
async def misc(bot, update):
    data = update.data.split("_")[-1]
    if data == "home":
        await update.message.edit(
            text=script.START.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ʜᴇʟᴘ", callback_data="misc_help"),
                                                InlineKeyboardButton("ʙᴜʏ", callback_data="misc_buymoney")]])
        )
    elif data == "help":
        await update.message.edit(
            text=script.HELP,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="misc_home")]])
        )
    elif data == "buymoney":
        await update.message.edit(
            text=script.BUY.format((await bot.get_me()).mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Qr", callback_data="buy_qr")],[
         InlineKeyboardButton("Upi", callback_data="buy_upi")],[
         InlineKeyboardButton("Mdisk Views", callback_data="buy_mdisk")]
    ])) 

         
@Client.on_message(filters.command("buy"))
async def buy(bot, message):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("QR", callback_data="buy_qr")],[
            InlineKeyboardButton("UPI", callback_data="buy_upi")],[
            InlineKeyboardButton("MDISK VIEWS", callback_data="buy_mdisk")]
        ])
        await message.reply("How do you want to pay?", reply_markup=keyboard)


@Client.on_callback_query(filters.regex(r"^buy"))
async def process_buy(bot, update):
    data = update.data.split("_")[-1]
    if data == "qr":
        # send photo
        photo_url = "https://telegra.ph/file/55432e3caf49188dc5d30.jpg"  # replace with your QR image URL
        await bot.send_photo(chat_id=update.message.chat.id, photo=photo_url)
        text = "Pay 10 Ruppe and then send a screenshot of the payment below, and also provide your group ID so I can verify After Sending Verification Request."
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Send Screenshot", url=f'https://t.me/Abdul_khalik_8')]
        ])
        await bot.send_message(chat_id=update.message.chat.id, text=text, reply_markup=keyboard)
    elif data == "upi":
        # send message and button
        text = "`sorry`\nPay 10 Ruppe and then send a screenshot of the payment below, and also provide your group ID After Sending Verification Request. can verify the payment."
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Send Screenshot", url=f'https://t.me/Abdul_khalik_8')]
        ])
        await bot.send_message(chat_id=update.message.chat.id, text=text, reply_markup=keyboard)
    elif data == "mdisk":
        # send message and button
        text = "Send 500 Mdisk Views To `5851749250` and then send a Message To The Bot Owner."
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Message", url=f'https://t.me/Abdul_khalik_8')]
        ])
        await bot.send_message(chat_id=update.message.chat.id, text=text, reply_markup=keyboard)

 
@Client.on_message(filters.command('leave') & filters.private &  filters.chat(ADMIN))
async def leave_a_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        chat = chat
    try:
        buttons = [[
            InlineKeyboardButton('𝚂𝚄𝙿𝙿𝙾𝚁𝚃', url=f'https://t.me/Abdul_khalik_8')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat,
            text='<b>Hello Friends, \nMy admin has told me to leave from group so i go! If you wanna add me again contact my support group.</b>',
            reply_markup=reply_markup,
        )

        await bot.leave_chat(chat)
        await message.reply(f"left the chat `{chat}`")
    except Exception as e:
        await message.reply(f'Error - {e}')

@Client.on_message(filters.command("gsend") & filters.private &  filters.chat(ADMIN))
async def send_chatmsg(bot, message):
    if message.reply_to_message:
        target_id = message.text
        command = ["/gsend"]
        for cmd in command:
            if cmd in target_id:
                target_id = target_id.replace(cmd, "")
        success = False
        try:
            chat = await bot.get_chat(int(target_id))
            await message.reply_to_message.copy(int(chat.id))
            success = True
        except Exception as e:
            await message.reply_text(f"<b>Eʀʀᴏʀ :- <code>{e}</code></b>")
        if success:
            await message.reply_text(f"<b>Yᴏᴜʀ Mᴇssᴀɢᴇ Hᴀs Bᴇᴇɴ Sᴜᴄᴇssғᴜʟʟʏ Sᴇɴᴅ To {chat.id}.</b>")
        else:
            await message.reply_text("<b>Aɴ Eʀʀᴏʀ Oᴄᴄᴜʀʀᴇᴅ !</b>")
    else:
        await message.reply_text("<b>Cᴏᴍᴍᴀɴᴅ Iɴᴄᴏᴍᴘʟᴇᴛᴇ...</b>")

@Client.on_chat_join_request(filters.group | filters.channel)
async def autoapprove(client, message: ChatJoinRequest):
    chat = message.chat 
    user = message.from_user 
    print(f"{user.first_name} joined (approved)") 
    await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
    if APPROVE == "on":
        await client.send_message(chat_id=chat.id, text=APPROVETEXT.format(mention=user.mention, title=chat.title))
