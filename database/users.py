import aiosqlite as sql

DATABASE = "bot.db"

async def addUser(ID: int, name: str, role: str = "student"):
    try:
        async with sql.connect(DATABASE) as con:
            await con.execute("""
                INSERT INTO users (id, name, role)
                VALUES (?, ?, ?)
            """, (ID, name, role))

            await con.commit()
            print(f"info: {name} added as {role}")
    except Exception as ex:
        print(f"error: failed to add user\n\nid: {ID}\nname: {name}\nrole: {role}\n\n{ex}")

async def getUserByID(ID: int):
    try:
        async with sql.connect(DATABASE) as con:
            async with con.execute("""
                SELECT id, name, role FROM users WHERE id = ?
            """, (ID,)) as cursor:
                user = await cursor.fetchone()
                print(f"info: received user with id: {ID}")
                return user
    except Exception as ex:
        print(f"error: failed to get user with id: {ID}\n\n{ex}")

async def getAllUsers():
    try:
        async with sql.connect(DATABASE) as con:
            async with con.execute("""
                SELECT id, name, role FROM users
            """) as cursor:
                rows = await cursor.fetchall()
                users = [
                    {"id": row[0], "name": row[1], "role": row[2]}
                    for row in rows
                ]
                print(f"info: retrieved all users")
                return users
    except Exception as ex:
        print(f"error: failed to retrieve all users\n\n{ex}")
        return []

async def userInDB(ID: int):
    try:
        async with sql.connect(DATABASE) as con:
            async with con.execute("""
                SELECT 1 FROM users WHERE id = ? LIMIT 1
            """, (ID,)) as cursor:
                result = await cursor.fetchone()
                print(f"info: check user with id: {ID}")
                return result is not None    
    except Exception as ex:
        print(f"error: failed to check user with id: {ID}\n\n{ex}")

async def updateUserRole(ID: int, role: str):
    try:
        async with sql.connect(DATABASE) as con:
            await con.execute("""
                UPDATE users SET role = ? WHERE id = ?
            """, (role, ID))

            await con.commit()
            print(f"info: user with id: {ID} updated to '{role}'")
    except Exception as ex:
        print(f"error: failed to update user to {role} with id: {ID}\n\n{ex}")

async def deleteUser(ID: int):
    try:
        async with sql.connect(DATABASE) as con:
            await con.execute("""
                DELETE FROM users WHERE id = ?
            """, (ID,))

            await con.commit()
            print(f"info: deleted user with id: {ID}")
    except Exception as ex:
        print(f"error: failed to delete user with id: {ID}\n\n{ex}")

async def getStudentIDs():
    try:
        async with sql.connect(DATABASE) as con:
            cur = await con.execute("SELECT id FROM users WHERE role = 'student'")
            rows = await cur.fetchall()
            student_ids = [row[0] for row in rows]
            print(f"info: retrieved student ids")
            return student_ids
    except Exception as ex:
        print(f"error: failed to retrieve student ids\n\n{ex}")
        return []

async def getAdminAndDeveloperIDs():
    try:
        async with sql.connect(DATABASE) as con:
            cur = await con.execute("SELECT id FROM users WHERE role IN ('admin', 'developer')")
            rows = await cur.fetchall()
            admin_dev_ids = [row[0] for row in rows]
            print(f"info: retrieved admin and developer ids")
            return admin_dev_ids
    except Exception as ex:
        print(f"error: failed to retrieve admin and developer ids\n\n{ex}")
        return []

