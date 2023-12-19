import requests
from bs4 import BeautifulSoup 
from .sql import DataBase
from datetime import datetime
from keyboards import url_kb
from settings import GROUPS
import pytz

class Jobs:
    __USD_RUB = "https://iss.moex.com/iss/engines/currency/markets/selt/boards/CETS/securities/USD000UTSTOM.jsonp?iss.meta=off&iss.only=securities,marketdata&lang=ru" #"https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E"
    __EUR_RUB = "https://iss.moex.com/iss/engines/currency/markets/selt/boards/CETS/securities/EUR_RUB__TOM.jsonp?iss.meta=off&iss.only=securities,marketdata&lang=ru"   #".https://www.google.com/search?q=%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E"
    __AMD_RUB = "https://iss.moex.com/iss/engines/currency/markets/selt/boards/CETS/securities/AMDRUB_TOM.jsonp?iss.meta=off&iss.only=securities,marketdata&lang=ru" #"https://www.google.com/search?q=%D0%B0%D1%80%D0%BC%D1%8F%D0%BD%D1%81%D0%BA%D0%B8%D0%B9+%D0%B4%D1%80%D0%B0%D0%BC+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E"
    __USD_AMD = "https://iss.moex.com/iss/engines/currency/markets/selt/boards/CETS/securities/USDAMD_TOM.jsonp?iss.meta=off&iss.only=securities,marketdata&lang=ru" 
    
    __MoskowFormat = pytz.timezone("Europe/Moscow") 

    *__URLS, = __USD_RUB, __EUR_RUB, __AMD_RUB, __USD_AMD
    
    __headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    
    __db = DataBase()

    __actual_values = [0,0,0,0]


    def __init__(self, bot):
        self.__bot = bot

    def __is_equal_lists(self, data, data2):
        i=0
        while(i < 4):
            if(data[i] !=data2[i]): return False
            i+=1
        return True


    def __parse(self, url):
        full_page = requests.get(url, headers=self.__headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll("ul", {"class": "mx-security-digest"})
        print(convert[0].text)
        return convert[0].text
    
    def __get_price(self, url):
        response = requests.get(url)
        _jsonp = response.json()
        mk = _jsonp['marketdata']['data']
        return float(mk[0][8])
    
    async def __update_description_group(self, values):
        for groupid in GROUPS:
            await self.__bot.set_chat_description(groupid, f"‼️АКТУАЛЬНЫЙ КУРС КАЖДЫЕ 15 МИНУТ\n\nUSD/RUB - {values[0]} ₽\nEUR/RUB - {values[1]} ₽\nAMD/RUB - {values[2]/100} ₽\nUSD/AMD - {values[3]} ֏\n\nГруппа создана с целью поиска выгодного варианта обмена валют без посредников.\n\n\n📣По всем вопросам @O_K_Kseniia")

    async def avto_posting(self):
        currentDateAndTime = datetime.now(self.__MoskowFormat).strftime("%m/%d/%Y, %H:%M:%S")
        for groupid in GROUPS:
            data = await self.__db.getRates()
            await self.__bot.send_message(groupid, f"‼️АКТУАЛЬНЫЙ КУРС‼️\n({currentDateAndTime})\n\nUSD/RUB - {data[1]} ₽\nEUR/RUB - {data[2]} ₽\nAMD/RUB - {data[3]} ₽\nUSD/AMD - {data[4]} ֏",disable_notification=True, reply_markup=url_kb)

    async def update_currency(self):
        currentDateAndTime = datetime.now(self.__MoskowFormat).strftime("%m/%d/%Y, %H:%M:%S")
        try:
            b = True
            values = []
            for url in self.__URLS:
                values.append(self.__get_price(url))
            if(self.__is_equal_lists(values,self.__actual_values) == False):
               self.__actual_values = values.copy()
               await self.__db.addRate(currentDateAndTime, values[0], values[1], values[2] / 100 , values[3])
               await self.__update_description_group(values)

        except Exception as e:
            print(e)




