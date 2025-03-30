import aiosqlite as sql

DATABASE = "bot.db"

async def addUnknown(ID: int, start_msg_id: int, username: str, name: str):
	try:
		async with sql.connect(DATABASE) as con:
			await con.execute("""
				INSERT INTO unknowns (id, start_msg_id, username, name)
				VALUES (?, ?, ?, ?)
			""", (ID, start_msg_id, username, name))

			await con.commit()
			print(f"info: added unknown:\n\nid: {ID}\nstart message id: {start_msg_id}\nusername: @{username}\nname: {name}\n")
	except Exception as ex:
		print(f"error: failed to add unknown\n\nid: {ID}\nstart message id: {start_msg_id}\nusername: @{username}\nname: {name}\n\n{ex}")

async def deleteUnknown(ID: int):
	try:
		async with sql.connect(DATABASE) as con:
			await con.execute("DELETE FROM unknowns WHERE id = ?", (ID,))

			await con.commit()
			print(f"info: deleted unknown with id: {ID}")
	except Exception as ex:
		print(f"error: failed to delete unknown with id: {ID}\n\n{ex}")

async def getAllUnknowns():
	try:
		async with sql.connect(DATABASE) as con:
			cur = await con.execute("SELECT id, username, name FROM unknowns")
			rows = await cur.fetchall()

			result = [{"id": row[0], "username": row[1], "name": row[2]} for row in rows]

			print(f"info: received a list of unknowns")
			return result	
	except Exception as ex:
		print(f"error: failed to get all unknowns\n\n{ex}")
		return []

async def inUnknowns(ID: int):
	try:
		async with sql.connect(DATABASE) as con:
			cur = await con.execute("SELECT 1 FROM unknowns WHERE id = ?", (ID,))
			result = await cur.fetchone()

			print(f"info: user with id: {ID} in unknowns is {result is not None}")
			return result is not None
	except Exception as ex:
		print(f"error: failed to check user with id: {ID} in unknowns\n\n{ex}")
		return False

async def updateSMID(userID: int, SMID: int):
	try:
		async with sql.connect(DATABASE) as con:
			await con.execute(
					"UPDATE unknowns SET start_msg_id = ? WHERE id = ?",
					(SMID, userID)
			)
			await con.commit()

		print(f"info: updated start message id for id: {userID}")

	except Exception as ex:
		print(f"error: failed to update start message id\n\nstart message id: {SMID}\nuser id: {userID}\n\n{ex}")

async def getSMID(userID: int):
	try:
		async with sql.connect(DATABASE) as con:
			cur = await con.execute("SELECT start_msg_id FROM unknowns WHERE id = ?", (userID,))
			row = await cur.fetchone()

			print(f"info: get start message id from id: {userID}")
			return row[0] if row else None

	except Exception as ex:
		print(f"error: failed to get start message id from id: {userID}")
		return False
