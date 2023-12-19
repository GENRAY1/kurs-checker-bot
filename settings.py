import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_FILE = "db"
GROUPS = (-1001735978971,) #-1001735978971