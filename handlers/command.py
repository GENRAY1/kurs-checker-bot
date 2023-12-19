from aiogram.types import Message, ChatType
from aiogram.dispatcher.filters import Command, BoundFilter, ChatTypeFilter
from main import bot,dp
from services import DataBase
from settings import GROUPS
import pytz

class IsGroup(BoundFilter):
    async def check(self, message: Message) -> bool:
        return message.chat.type in (
            ChatType.SUPERGROUP,
        )
    
class IsOurGroup(BoundFilter):
    async def check(self, message: Message) -> bool:
        return message.chat.id in GROUPS
    
MoskowFormat = pytz.timezone("Europe/Moscow") 
db = DataBase()

@dp.message_handler(IsGroup(), IsOurGroup(),Command('check'))
async def check_in_group(message: Message):
    d = message.date.strftime("%d/%m/%Y, %H:%M:%S")
    data = await db.getRates()
    await bot.send_message(message.chat.id, f"‼️АКТУАЛЬНЫЙ КУРС‼️\n({d})\n\nUSD/RUB - {data[1]} ₽\nEUR/RUB - {data[2]} ₽\nAMD/RUB - {data[3]} ₽\nUSD/AMD - {data[4]} ֏",disable_notification=True)

@dp.message_handler(ChatTypeFilter(chat_type=ChatType.PRIVATE), commands=['start', 'check'])
async def check_in_private(message:Message):
    d = message.date.strftime("%d/%m/%Y, %H:%M:%S")
    data = await db.getRates()
    await bot.send_message(message.chat.id, f"‼️АКТУАЛЬНЫЙ КУРС‼️\n({d})\n\nUSD/RUB - {data[1]} ₽\nEUR/RUB - {data[2]} ₽\nAMD/RUB - {data[3]} ₽\nUSD/AMD - {data[4]} ֏",disable_notification=True)