from aiogram import Router
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram import F
from aiogram.fsm.context import FSMContext

from filters import IsDeveloper
from keyboards.admin import admAdmKb, backKb

from handlers.admin import admStates


router = Router()


#@router.message(F.text == 'Админка🔒', IsDeveloper())
#async def dvlpMenuCmd(message: Message):
#	await message.answer("Админка", reply_markup=admAdmKb())

#@router.message(F.text == 'Изменить расписание', IsDeveloper())
#async def newTimetable(message: Message, state: FSMContext):
#	await state.set_state(States.timetable)
#	await message.answer("Отправьте новое расписание", reply_markup=backKb())

