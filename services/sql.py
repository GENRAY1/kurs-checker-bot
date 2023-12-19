import sqlite3;
from settings import DB_FILE
class DataBase:
    def __init__(self):
        self.connect = sqlite3.connect(DB_FILE)
        self.cursor = self.connect.cursor()
    
    async def getRates(self):
        with self.connect:
            return self.cursor.execute('''SELECT [date], [usd/rub], [eur/rub], [amd/rub], [usd/amd] FROM CurrencyRates 
            ORDER BY [id] DESC LIMIT 1''').fetchall()[0]
        
    async def addRate(self, date, usd_rub, eur_rub, amd_rub, usd_amd):
        with self.connect:
            return self.cursor.execute('''INSERT INTO CurrencyRates([date],[usd/rub],[eur/rub],[amd/rub],[usd/amd]) VALUES(?,?,?,?,?)''',
                                       [date, usd_rub, eur_rub, amd_rub, usd_amd])
            