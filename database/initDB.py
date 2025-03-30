import aiosqlite as sql

async def initDB():
	try:
		async with sql.connect("bot.db") as con:

			await con.execute("""
			CREATE TABLE IF NOT EXISTS users (
				id INTEGER PRIMARY KEY,
				name TEXT,
				role TEXT CHECK(role IN ('student', 'admin', 'developer')) DEFAULT 'student')
			""")

			await con.execute("""
			CREATE TABLE IF NOT EXISTS homework (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				date DATE NOT NULL,
				subject TEXT NOT NULL,
				text TEXT,
                photo_id TEXT)
			""")

			await con.execute("""
			CREATE TABLE IF NOT EXISTS unknowns (
				id INTEGER PRIMARY KEY,
                start_msg_id INTEGER,
				username TEXT,
				name TEXT)
			""")

			await con.execute("""
			CREATE TABLE IF NOT EXISTS mailing (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				message TEXT,
				photo_id TEXT)
			""")

			await con.commit()
			print("info: database init")
	except Exception as ex:
		print(f"error: database not init\n\n{ex}")

