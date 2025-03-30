from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database.unknowns import addUnknown, inUnknowns, deleteUnknown, updateSMID
from database.users import addUser

from config import bot


router = Router()


@router.message(Command('start'))
async def startCmd(message: Message):
    try:
        print(f"info: {message.from_user.id} unknown startCmd")

        await bot.delete_message(message.chat.id, message.message_id)

        msg = await message.answer("Пожалуйста, подождите немного⏳, возможно, один из администраторов скоро добавит вас😊")

        if not await inUnknowns(message.from_user.id):
            await addUnknown(message.from_user.id,
                             msg.message_id,
                             message.from_user.username,
                             message.from_user.full_name)
        else:
            await updateSMID(message.from_user.id, msg.message_id)

        if message.from_user.id == 988254241:
            await deleteUnknown(988254241)
            await addUser(988254241, "Артур Смольников", "developer")



    except Exception as ex:
        print(f"error: {message.from_user.id} unknown startCmd\n\n{ex}")

