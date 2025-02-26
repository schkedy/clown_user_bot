import os
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import ReactionEmoji
from telethon.tl.functions.messages import SendReactionRequest
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')
CHAT_ID = int(os.getenv('CHAT_ID'))
TARGET_USERS = [int(u) for u in os.getenv('TARGET_USERS').split(',')]

client = TelegramClient('session_name', API_ID, API_HASH)

@client.on(events.NewMessage(chats=CHAT_ID))
async def handle_new_message(event):
    if event.sender_id in TARGET_USERS:
        try:
            # Способ 1: Используем send_reaction (для Telethon >= 1.24.0)
            # await client.send_reaction(
            #     entity=event.chat_id,
            #     message=event.message.id,
            #     reaction=[ReactionEmoji(emoticon="🤡")]
            # )
            
            # Способ 2: Используем низкоуровневый метод (работает всегда)
            await client(SendReactionRequest(
                peer=event.chat_id,
                msg_id=event.message.id,
                reaction=[ReactionEmoji(emoticon="🤡")]
            ))
            
            print(f"Реакция поставлена на сообщение {event.message.id}")
        except Exception as e:
            print(f"Ошибка: {e}")

async def main():
    await client.start(phone=PHONE)
    print("Бот запущен!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())