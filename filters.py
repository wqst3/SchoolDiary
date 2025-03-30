from aiogram.types import Message, ContentType
from aiogram.filters import Filter

from database.users import getUserByID


class IsStudent(Filter):
	async def __call__(self, message: Message) -> bool:
		user = await getUserByID(message.from_user.id)
		if not user:
			return False
		return "student" == user[2]

class IsAdmin(Filter):
	async def __call__(self, message: Message) -> bool:
		user = await getUserByID(message.from_user.id)
		if not user:
			return False
		return "admin" == user[2]

class IsDeveloper(Filter):
	async def __call__(self, message: Message) -> bool:
		user = await getUserByID(message.from_user.id)
		if not user:
			return False
		return "developer" == user[2]

class NotStudent(Filter):
	async def __call__(self, message: Message) -> bool:
		user = await getUserByID(message.from_user.id)
		if not user:
			return False
		return user[2] == "developer" or user[2] == "admin"

class NotUnknown(Filter):
	async def __call__(self, message: Message) -> bool:
		user = await getUserByID(message.from_user.id)
		return True if user else False

class IsPhoto(Filter):
	async def __call__(self, message: Message) -> bool:
		return message.content_type == ContentType.PHOTO

class IsText(Filter):
	async def __call__(self, message: Message) ->bool:
		return bool(message.text)
