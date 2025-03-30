import asyncio

from handlers import student, admin, developer, unknown

from config import bot, dp

from database.initDB import initDB


async def main() -> None:

	dp.include_router(student.router)
	dp.include_router(admin.router)
	dp.include_router(developer.router)
	dp.include_router(unknown.router)

	await initDB()
	await bot.delete_webhook(True)
	await dp.start_polling(bot)


if __name__ == '__main__':
	asyncio.run(main())

