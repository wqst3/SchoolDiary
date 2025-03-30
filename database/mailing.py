import aiosqlite as sql

DATABASE = "bot.db"

async def addMessage(message: str = None, photo_id: str = None):
	try:
		async with sql.connect(DATABASE) as con:
			await con.execute(
				"INSERT INTO mailing (message, photo_id) VALUES (?, ?)", 
				(message, photo_id)
			)
			await con.commit()
			print(f"info: add message to mailing")
	except Exception as ex:
		print(f"error: failed to add message to mailing\n\n{ex}")

async def getMailing():
	try:
		async with sql.connect(DATABASE) as con:
			async with con.execute("SELECT id, message, photo_id FROM mailing") as cur:
				rows = await cur.fetchall()
				result = {row[0]: (row[1], row[2]) for row in rows}	
				print("info: get all messages from mailing")
				return result
	except Exception as ex:
		print(f"error: failed to get messages from mailing\n\n{ex}")
		return {}

async def deleteMessage(ID: int):
	try:
		async with sql.connect(DATABASE) as con:
			await con.execute("DELETE FROM mailing WHERE id = ?", (ID,))
			await con.commit()
			print(f"info: deleted message from mailing with id: {ID}")
	except Exception as ex:
		print(f"error: failed to delete message from mailing with id: {ID}\n\n{ex}")

