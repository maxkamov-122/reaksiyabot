#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import random
import logging
from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji

# ==================== SOZLAMALAR ====================
API_ID = 37633950
API_HASH = "a8bdabe9590a792bc50d993a6da88189"
PHONE_NUMBER = "+998971216115"  # TELEFON RAQAMINGIZNI YOZING!

# Random emojilar ro'yxati
EMOJI_LIST = ["\U0001F44D", "\u2764\ufe0f", "\U0001F525"]

# ==================== LOGGING ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== USERBOT YARATISH ====================
client = TelegramClient('userbot_session', API_ID, API_HASH)

# ==================== YORDAMCHI FUNKSIYA ====================
def get_random_emoji():
    """Tasodifiy emoji qaytaradi"""
    return random.choice(EMOJI_LIST)

# ==================== ASOSIY REAKSIYA MANTIQI ====================
@client.on(events.NewMessage)
async def react_to_post(event):
    """
    Siz a'zo bo'lgan HAR QANDAY kanal yoki guruhdagi yangi postga random reaksiya bosadi
    """
    try:
        # O'z xabarlarimizga reaksiya bosmaymiz
        if event.out:
            return
        
        # Tasodifiy emoji tanlash
        emoji = get_random_emoji()
        
        # Reaksiya bosish
        await client(SendReactionRequest(
            peer=event.chat_id,
            msg_id=event.id,
            reaction=[ReactionEmoji(emoticon=emoji)]
        ))
        
        chat_title = event.chat.title if hasattr(event.chat, 'title') else event.chat_id
        logger.info(f"✅ Reaksiya: {emoji} -> {chat_title}")
        
    except Exception as e:
        logger.error(f"❌ Xatolik: {e}")

# ==================== STARTUP XABARI ====================
@client.on(events.NewMessage(pattern='/start', outgoing=True))
async def start_handler(event):
    await event.edit(
        "🤖 **Userbot Ishga Tushdi!**\n\n"
        "🎯 **Ishlash tartibi:**\n"
        f"• Siz a'zo bo'lgan barcha kanal/guruhlardagi yangi postlarga random reaksiya bosiladi\n"
        f"• Random emojilar soni: {len(EMOJI_LIST)} ta\n\n"
        "⚡ **Buyruqlar:**\n"
        "• `/stats` - Statistika\n"
        "• `/emojis` - Emojilar ro'yxati\n"
        "• `/stop` - Userbotni to'xtatish"
    )

# ==================== STATS ====================
@client.on(events.NewMessage(pattern='/stats', outgoing=True))
async def stats_handler(event):
    dialogs = await client.get_dialogs()
    channels = [d for d in dialogs if d.is_channel]
    groups = [d for d in dialogs if d.is_group]
    
    text = f"📊 **Userbot Statistikasi**\n\n"
    text += f"📢 Kanallar: {len(channels)} ta\n"
    text += f"👥 Guruhlar: {len(groups)} ta\n"
    text += f"🔗 Jami chatlar: {len(channels) + len(groups)} ta\n"
    text += f"🎲 Random emojilar: {len(EMOJI_LIST)} ta"
    
    await event.edit(text)

# ==================== EMOJIS ====================
@client.on(events.NewMessage(pattern='/emojis', outgoing=True))
async def emojis_handler(event):
    emoji_text = " ".join(EMOJI_LIST)
    await event.edit(
        f"🎲 **Random emojilar ro'yxati** ({len(EMOJI_LIST)} ta):\n\n"
        f"{emoji_text}"
    )

# ==================== STOP ====================
@client.on(events.NewMessage(pattern='/stop', outgoing=True))
async def stop_handler(event):
    await event.edit("🛑 **Userbot to'xtatilmoqda...**")
    await client.disconnect()

# ==================== USERBOTNI ISHGA TUSHIRISH ====================
async def main():
    print("=" * 50)
    print("🤖 USERBOT ISHGA TUSHMOQDA...")
    print("=" * 50)
    
    await client.start(phone=PHONE_NUMBER)
    
    me = await client.get_me()
    print(f"✅ Akkaunt: @{me.username or me.first_name}")
    print(f"🎲 Random emojilar: {len(EMOJI_LIST)} ta")
    print(f"📢 Siz a'zo bo'lgan barcha chatlarda ishlaydi")
    print("-" * 50)
    print("⚡ /stop - to'xtatish")
    print("=" * 50)
    
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Userbot to'xtatildi.")