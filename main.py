from settings import BOT_TOKEN
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from services import Jobs

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)
scheduler = AsyncIOScheduler()
jobs = Jobs(bot)


scheduler.add_job(jobs.update_currency, "interval", seconds=300, misfire_grace_time=None)
#scheduler.add_job(jobs.avto_posting, "interval", seconds=360, misfire_grace_time=None)
scheduler.add_job(jobs.avto_posting, 'cron', hour=10, minute=30, misfire_grace_time=None)
scheduler.add_job(jobs.avto_posting, 'cron', hour=15, minute=30, misfire_grace_time=None)
scheduler.add_job(jobs.avto_posting, 'cron', hour=19, minute=30, misfire_grace_time=None)
async def main():
    from handlers import dp
    try:
       scheduler.start()
       await dp.start_polling()
    finally:
        await bot.session.close() 

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except(KeyboardInterrupt, SystemExit):
       print("stopped") 