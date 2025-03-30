from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F

from database.users import userInDB, addUser, getUserByID, getAdminAndDeveloperIDs
from database.homework import getHomeworkByDate

from keyboards.student import menuKb, homeworkKb, homeworkIKb
from keyboards.admin import admMenuKb, backKb

from states import States, admStates

from filters import NotUnknown

from config import bot

from datetime import datetime, timedelta

import locale


locale.setlocale(locale.LC_TIME, "ru_RU.utf8")

router = Router()
router.message.filter(NotUnknown())


@router.message(F.text == '🔙 Назад', States.homework)
@router.message(F.text == "🔙 Назад", States.support)
@router.message(F.text == "🔙 Назад", admStates.admin)
@router.message(F.text == '🔙 Назад', admStates.homework)
@router.message(F.text == '🔙 Назад', admStates.mailing)
@router.message(F.text == '🔙 Назад', admStates.usersModify)
@router.message(Command('start'))
async def startCmd(message: Message, state: FSMContext):

	await state.set_state(States.student)
	userID = message.from_user.id

	if await userInDB(userID):
		user = await getUserByID(userID)

		if user[2] == "student":
			await message.answer("<b>Дневник 10А Школы №17</b>\n\n📋 Главное меню", parse_mode='HTML', reply_markup=menuKb())
			print("info: student start command")
		elif user[2] in ("admin", "developer"):
			await message.answer("<b>Дневник 10А Школы №17</b>\n\n📋 Главное меню", parse_mode='HTML', reply_markup=admMenuKb())
			print("info: admin start command")


@router.message(F.text == "📅 Расписание", States.homework)
@router.message(F.text == "📅 Расписание", States.student)
async def timetableCmd(message: Message, state: FSMContext):
	await state.set_state(States.student)

	try:
		photo = FSInputFile("timetable.jpg")

		await message.answer_photo(photo)
		print("info: send timetable")
	except FileNotFoundError:
		await message.answer("Расписания ещё нет")
		print("info: not timetable in directory")
	except Exception as ex:
		await message.answer("Неизвестная ошибка")
		print(f"error: timetable sending error\n{ex}")


async def delete_old_messages(message, state):
	data = await state.get_data()
	message_ids = data.get("message_ids", [])

	for msg_id in message_ids:
		try:
			await message.bot.delete_message(message.chat.id, msg_id)
		except Exception:
			pass

def get_next_weekday(date_obj, direction=1):
	if date_obj.weekday() == 6:
		date_obj += timedelta(days=direction)
	return date_obj


@router.message(F.text == "📝 Домашние задания", States.homework)
@router.message(F.text == "📝 Домашние задания", States.student)
async def show_homework(message, state):
	await state.clear()
	await state.set_state(States.homework)

	today = datetime.today()
	today = get_next_weekday(today)
	today_str = today.strftime("%Y-%m-%d")
	
	await send_homework(message, state, today_str)

def format_date(date_str):
	date_obj = datetime.strptime(date_str, "%Y-%m-%d")
	return date_obj.strftime("%d %B %Y")

async def send_homework(message, state, date):

		print("info: send_homework")

		await delete_old_messages(message, state)

		new_message_ids = []

		homework = await getHomeworkByDate(date)

		if homework == []:
			hm_msg = await message.answer("<b>Нет домашнего задания</b>", parse_mode='HTML')
		else:
			hm_msg = await message.answer("<b>📝 Домашние задания</b>", parse_mode='HTML')

		new_message_ids.append(hm_msg.message_id)
		
		for h in homework:
			if h[3]:
				msg = await message.answer_photo(h[3], f"<b>{h[1]}</b>\n\n{h[2]}", parse_mode='HTML')
			else:
				msg = await message.answer(f"<b>{h[1]}</b>\n\n{h[2]}", parse_mode='HTML')

			new_message_ids.append(msg.message_id)

		formatted_date = datetime.strptime(date, "%Y-%m-%d").date().strftime("%-d %B | %A")

		date_msg = await message.answer(text=f"<b>{formatted_date}</b>", parse_mode='HTML', reply_markup=homeworkIKb(date))

		new_message_ids.append(date_msg.message_id)

		await state.update_data(message_ids=new_message_ids, current_date=date)


@router.callback_query(lambda c: c.data.startswith("select_date:"), States.homework)
async def change_day(callback_query: CallbackQuery, state):
	selected_date = callback_query.data.split(":")[1]
	await state.update_data(current_date=selected_date)
	await send_homework(callback_query.message, state, selected_date)
	await callback_query.answer()

@router.callback_query(lambda c: c.data.startswith("change_week:"), States.homework)
async def change_week(callback_query: CallbackQuery, state: FSMContext):
	new_week_start = callback_query.data.split(":")[1]
	new_week_start = datetime.strptime(new_week_start, "%Y-%m-%d").date()

	await callback_query.message.edit_reply_markup(reply_markup=homeworkIKb(new_week_start))
	await callback_query.answer()


@router.message(F.text == "🛠️ Поддержка", States.homework)
@router.message(F.text == "🛠️ Поддержка", States.student)
async def support(message: Message, state: FSMContext):
	await state.set_state(States.support)
	await message.answer("📩 Если у вас есть <b>вопрос</b> или <b>проблема</b>, напишите нам!", 
						parse_mode='HTML', reply_markup=backKb())


@router.message(States.support)
async def supportEnd(message: Message, state: FSMContext):
	await state.set_state(States.student)

	admins = await getAdminAndDeveloperIDs()
	user = await getUserByID(message.from_user.id)

	user_info = f"📩 <b>Сообщение от {user[1]}</b>"
	caption = message.caption if message.caption else ""

	if user[2] in ['admin', 'developer']:

		for admin in admins:
			if admin != message.from_user.id:
				if message.text:
					await bot.send_message(admin, f"{user_info}\n\n{message.text}", parse_mode='HTML')
				elif message.photo:
					await bot.send_photo(admin, message.photo[-1].file_id, caption=f"{user_info}\n\n{caption}", parse_mode='HTML')
				elif message.video:
					await bot.send_video(admin, message.video.file_id, caption=f"{user_info}\n\n{caption}", parse_mode='HTML')

		await message.answer("✅ Ваше сообщение отправлено в поддержку", reply_markup=admMenuKb())

	else:

		for admin in admins:

			if message.text:
				await bot.send_message(admin, f"{user_info}\n\n{message.text}", parse_mode='HTML')
			elif message.photo:
				await bot.send_photo(admin, message.photo[-1].file_id, caption=f"{user_info}\n\n{caption}", parse_mode='HTML')
			elif message.video:
				await bot.send_video(admin, message.video.file_id, caption=f"{user_info}\n\n{caption}", parse_mode='HTML')

		await message.answer("✅ Ваше сообщение отправлено в поддержку", reply_markup=menuKb())
