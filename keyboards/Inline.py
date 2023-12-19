from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


url_btn1 = InlineKeyboardButton("Проверить курс валют", url="https://t.me/removelinksbot?start=check")

url_kb = InlineKeyboardMarkup()
url_kb.add(url_btn1)