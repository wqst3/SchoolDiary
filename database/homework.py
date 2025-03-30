import aiosqlite as sql

DATABASE = "bot.db"

async def addHomework(date: str, subject: str, text: str = None, photo_id: str = None):
	try:
		async with sql.connect(DATABASE) as con:
			await con.execute("""
				INSERT INTO homework (date, subject, text, photo_id) VALUES (?, ?, ?, ?)
			""", (date, subject, text, photo_id))

			await con.commit()
			print(f"info: added homework\n\ndate: {date}\nsubject: {subject}\ntext: {text}\nphoto_id: {photo_id}\n")
	except Exception as ex:
		print(f"info: added homework\n\ndate: {date}\nsubject: {subject}\ntext: {text}\nphoto_id: {photo_id}\n")

async def getHomeworkByDate(date: str):
	try:
		async with sql.connect(DATABASE) as con:
			async with con.execute("""
				SELECT id, subject, text, photo_id FROM homework WHERE date = ?
			""", (date,)) as cursor:

				homework_list = await cursor.fetchall()
				return homework_list

			print("info: received all homework for the {date}")
	except Exception as ex:
		print(f"error: failed to get homework assignment for the {date}\n\n{ex}")

async def getHomeworkBySubject(subject: str):
	try:
		async with sql.connect(DATABASE) as con:
			async with con.execute("""
				SELECT id, subject, text, photo_id FROM homework WHERE subject = ?
			""", (subject,)) as cursor:

				homework_list = await cursor.fetchall()
				return homework_list

			print("info: received all {subject} homework")
	except Exception as ex:
		print("error: failed to get all {subject} homework")

async def deleteHomeworkByID(ID: int):
	try:
		async with sql.connect(DATABASE) as con:
			await con.execute("""
				DELETE FROM homework WHERE id = ?
			""", (ID,))

			await con.commit()
			print(f"info: deleted homework with id: {ID}")
	except Exception as ex:
		print(f"error: failed to delete homework with id: {ID}\n\n{ex}")

