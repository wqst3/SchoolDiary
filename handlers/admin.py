from aiogram import Router
from aiogram.types import CallbackQuery, Message, ContentType, User, Chat, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import F
from aiogram.fsm.context import FSMContext

from filters import IsAdmin, IsDeveloper, IsPhoto, NotStudent, IsText

from keyboards.admin import admAdmKb, backKb, backIKb, admMenuKb, chooseRoleKb, deletePersonKb, deleteButtonIKb, mailingIKb, deleteUserButtonIKb, addUserButtonIKb, homeworkKb, admWeekCalendarIkb
from keyboards.student import subjectIKb, menuKb, homeworkIKb

from states import States, admStates

from config import bot

from database.unknowns import getAllUnknowns, inUnknowns, deleteUnknown, getSMID
from database.users import addUser, getStudentIDs, getAdminAndDeveloperIDs, getAllUsers, userInDB, getUserByID, deleteUser
from database.mailing import addMessage, getMailing, deleteMessage
from database.homework import addHomework, getHomeworkByDate, deleteHomeworkByID

from handlers.student import startCmd

import asyncio

import datetime

import locale


router = Router()
router.message.filter(NotStudent())


# ПЕРВЫЙ УРОВЕНЬ

@router.message(F.text == '🔒 Админка', States.student)
@router.message(F.text == '🔒 Админка', States.homework)
@router.message(F.text == '🔙 Назад', admStates.timetable)
@router.message(F.text == '🔙 Назад', admStates.newPerson)
@router.message(F.text == '🔙 Назад', admStates.deletePerson)
async def admMenuCmd(message: Message, state: FSMContext):
	await state.set_state(admStates.admin)

	await message.answer("<b>Дневник 10А Школы №17</b>\n\n🔒 Админ меню", parse_mode='HTML', reply_markup=admAdmKb())

	print("info: admMenuCmd")


# ВТОРОЙ УРОВЕНЬ(АДМИН МЕНЮ)
@router.message(F.text == '📅 Изменить расписание', admStates.usersModify)
@router.message(F.text == '📅 Изменить расписание', admStates.homework)
@router.message(F.text == '📅 Изменить расписание', admStates.mailing)
@router.message(F.text == '📅 Изменить расписание', admStates.admin)
async def newTimetable(message: Message, state: FSMContext):
	await state.clear()
	await state.set_state(admStates.timetable)

	await message.answer("🆕 Отправьте новое расписание", reply_markup=backKb())

	print("info: newTimetable command")


async def delete_old_messages(chat_id, state):
	data = await state.get_data()
	message_ids = data.get("message_ids", [])

	for msg_id in message_ids:
		try:
			await bot.delete_message(chat_id, msg_id)
		except Exception:
			pass

def get_next_weekday(date_obj, direction=1):
	if date_obj.weekday() == 6:
		date_obj += timedelta(days=direction)
	return date_obj

@router.message(F.text == "📝 Изменить Д/З", admStates.usersModify)
@router.message(F.text == "📝 Изменить Д/З", admStates.admin)
@router.message(F.text == "📝 Изменить Д/З", admStates.homework)
@router.message(F.text == "📝 Изменить Д/З", admStates.mailing)
async def homework(message: Message, state: FSMContext):
	await state.clear()
	await state.set_state(admStates.homework)

	today = datetime.datetime.today()
	today = get_next_weekday(today)
	today_str = today.strftime("%Y-%m-%d")
	
	await adm_send_homework(message, state, today_str)

@router.callback_query(lambda c: c.data == "back", admStates.subjectHomework)
async def homework(callback: CallbackQuery, state: FSMContext):
	await state.set_state(admStates.homework)

	today = datetime.datetime.today()
	today = get_next_weekday(today)
	today_str = today.strftime("%Y-%m-%d")
	
	await adm_send_homework(callback.message, state, today_str)

def format_date(date_str):
	date_obj = datetime.strptime(date_str, "%Y-%m-%d")
	return date_obj.strftime("%d %B %Y")

async def adm_send_homework(message, state, date):

		print("info: adm_send_homework")

		await delete_old_messages(message.chat.id, state)

		new_message_ids = []

		homework = await getHomeworkByDate(date)

		if homework == []:
			hm_msg = await message.answer("<b>Нет домашнего задания</b>", parse_mode='HTML')
		else:
			hm_msg = await message.answer("<b>📝 Домашние задания</b>", parse_mode='HTML')

		new_message_ids.append(hm_msg.message_id)
		
		for h in homework:
			delete_button = InlineKeyboardMarkup(
					inline_keyboard=[[InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_homework:{h[0]}")]]
			)
			if h[3]:
				msg = await message.answer_photo(h[3], f"<b>{h[1]}</b>\n\n{h[2]}", parse_mode='HTML', reply_markup=delete_button)
			else:
				msg = await message.answer(f"<b>{h[1]}</b>\n\n{h[2]}", parse_mode='HTML', reply_markup=delete_button)

			new_message_ids.append(msg.message_id)

		formatted_date = datetime.datetime.strptime(date, "%Y-%m-%d").date().strftime("%-d %B | %A")

		date_msg = await message.answer(text=f"<b>{formatted_date}</b>", parse_mode='HTML', reply_markup=admWeekCalendarIkb(date))

		new_message_ids.append(date_msg.message_id)

		await state.update_data(message_ids=new_message_ids, current_date=date)

@router.callback_query(lambda c: c.data.startswith("select_date:"), admStates.homework)
async def change_day(callback_query: CallbackQuery, state):
	selected_date = callback_query.data.split(":")[1]
	await state.update_data(current_date=selected_date)
	await adm_send_homework(callback_query.message, state, selected_date)
	await callback_query.answer()

@router.callback_query(lambda c: c.data.startswith("change_week:"), admStates.homework)
async def change_week(callback_query: CallbackQuery, state: FSMContext):
	new_week_start = callback_query.data.split(":")[1]
	new_week_start = datetime.datetime.strptime(new_week_start, "%Y-%m-%d").date()

	await callback_query.message.edit_reply_markup(reply_markup=admWeekCalendarIkb(new_week_start))
	await callback_query.answer()

@router.callback_query(lambda c: c.data.startswith("delete_homework"), admStates.homework)
async def delete_homework_callback(callback_query: CallbackQuery, state: FSMContext):
	homework_id = callback_query.data.split(":")[1]

	data = await state.get_data()
	current_date = data.get("current_date", datetime.date.today().strftime("%Y-%m-%d"))

	await deleteHomeworkByID(homework_id)

	await adm_send_homework(callback_query.message, state, current_date)


@router.message(F.text == '📢 Рассылка', admStates.usersModify)
@router.message(F.text == '📢 Рассылка', admStates.admin)
@router.message(F.text == '📢 Рассылка', admStates.homework)
@router.message(F.text == '📢 Рассылка', admStates.mailing)
async def mailingCmd(message: Message, state: FSMContext):
	await state.clear()

	await adm_send_mailing(message, state)

@router.message(F.text == '🔙 Назад', admStates.addMail)
async def mailingBack(message: Message, state: FSMContext):
	data = await state.get_data()
	message_ids = data.get("message_ids", [])
	message_ids.append(message.message_id)

	await state.update_data(message_ids=message_ids)

	await adm_send_mailing(message, state)

async def adm_send_mailing(message, state):
	await state.set_state(admStates.mailing)

	await delete_old_messages(message.chat.id, state)
	new_message_ids = []

	mailing = await getMailing()

	if mailing:
		msg = await message.answer("📢 <b>Сообщения для рассылки</b>", parse_mode="HTML", reply_markup=admAdmKb())
		new_message_ids.append(msg.message_id)

		for msg_id, (msg_text, photo_id) in mailing.items():
			if photo_id:
				msg = await message.answer_photo(photo_id, caption=msg_text, reply_markup=deleteButtonIKb(msg_id), parse_mode="HTML")
				new_message_ids.append(msg.message_id)
			else:
				msg = await message.answer(msg_text, reply_markup=deleteButtonIKb(msg_id), parse_mode="HTML")
				new_message_ids.append(msg.message_id)
	else:
		msg = await message.answer("📭 <b>Сообщений для рассылки нет</b>", parse_mode="HTML", reply_markup=admAdmKb())
		new_message_ids.append(msg.message_id)

	msg = await message.answer("Выберите действие для рассылки:", parse_mode="HTML", reply_markup=mailingIKb())
	new_message_ids.append(msg.message_id)

	await state.update_data(message_ids=new_message_ids)


@router.message(F.text == '👤 Изменить участников', admStates.usersModify)
@router.message(F.text == '👤 Изменить участников', admStates.homework)
@router.message(F.text == '👤 Изменить участников', admStates.mailing)
@router.message(F.text == '👤 Изменить участников', admStates.admin)
async def usersModify(message: Message, state: FSMContext):
	await state.clear()

	await adm_send_users(message, state)

@router.message(F.text == "🔙 Назад", admStates.enterName)
async def backUsersModify(message: Message, state: FSMContext):
	data = await state.get_data()
	message_ids = data.get("message_ids", [])
	message_ids.append(message.message_id)

	await adm_send_users(message, state)

async def adm_send_users(message, state):
	await state.set_state(admStates.usersModify)

	await delete_old_messages(message.chat.id, state)
	new_message_ids = []

	unknowns = await getAllUnknowns()

	if unknowns:
		msg = await message.answer("📋 <b>Список заявок:</b>", parse_mode='HTML', reply_markup=admAdmKb())
		new_message_ids.append(msg.message_id)

		for i, user in enumerate(unknowns, start=1):
			text = (
					f"<b>Юзернейм:</b> @{user['username'] if user['username'] else 'не указан'}\n"
					f"<b>Имя:</b> {user['name']}\n\n"
					)
			msg = await message.answer(text, parse_mode="HTML", reply_markup=addUserButtonIKb(user['id']))
			new_message_ids.append(msg.message_id) 
	else:
		msg = await message.answer("<b>🙅 Список заявок пуст</b>", parse_mode="HTML", reply_markup=admAdmKb())
		new_message_ids.append(msg.message_id)

	users = await getAllUsers()

	if users:
		msg = await message.answer("📋 <b>Список участников:</b>", parse_mode='HTML', reply_markup=admAdmKb())
		new_message_ids.append(msg.message_id)

		for user in users:
			text = ( 
					f"<b>Имя:</b> {user['name']}\n"
					f"<b>Роль:</b> {user['role'].capitalize()}\n\n"
					)
			msg = await message.answer(text, parse_mode="HTML", reply_markup=deleteUserButtonIKb(user['id']))
			new_message_ids.append(msg.message_id)
	else:
		msg = await message.answer("<b>🙅 Список участников пуст</b>", parse_mode="HTML", reply_markup=admAdmKb())
		new_message_ids.append(msg.message_id)

	await state.update_data(message_ids=new_message_ids)


# ИЗМЕНИТЬ РАСПИСАНИЕ

@router.message(admStates.timetable, IsPhoto())
async def newTimetable2(message: Message, state: FSMContext):
	try:
		photo_sizes = message.photo
		largest_photo = photo_sizes[-1]

		file_info = await message.bot.get_file(largest_photo.file_id)

		file_name = "timetable.jpg"
		await message.bot.download_file(file_info.file_path, destination=file_name)

		await state.set_state(admStates.admin)
		await message.answer("✅ Расписание изменено", reply_markup=admAdmKb())
		print(f"info: new timetable")
	except Exception as ex:
		print(f"error: error when saving a photo\n{ex}")
		await message.answer("Неизвестная ошибка")


# ИЗМЕНИТЬ Д/З(ВТОРОЙ УРОВЕНЬ)

@router.callback_query(lambda c: c.data == "add_homework", admStates.homework)
@router.callback_query(lambda c: c.data == "back", admStates.textHomework)
async def add_homework(callback: CallbackQuery, state: FSMContext):
	try:
		print("info: add_homework")

		await delete_old_messages(callback.message.chat.id, state)

		await state.set_state(admStates.subjectHomework)

		msg = await callback.message.answer("Выберите предмет:", reply_markup=subjectIKb())
		await state.update_data(message_ids=[msg.message_id])

		callback.answer()

	except Exception as ex:
		print(f"error: fail in add_homework\n{ex}")


# ИЗМЕНИТЬ Д/З(ТРЕТИЙ УРОВЕНЬ)

@router.callback_query(F.data.startswith("subject:"), admStates.subjectHomework)
async def select_subject(callback: CallbackQuery, state: FSMContext):

	await delete_old_messages(callback.message.chat.id, state)

	subject = callback.data.split(":")[1]
	await state.update_data(subject=subject)

	await state.set_state(admStates.textHomework)

	data = await state.get_data()
	current_date = datetime.datetime.strptime(data.get("current_date"), "%Y-%m-%d").strftime("%d.%m.%Y")

	msg = await callback.message.answer(f"<b>Дата:</b> {current_date}\n<b>Предмет:</b> {subject}\n✏️ Отправьте задание для домашней работы:",
										parse_mode = "HTML",
										reply_markup=backIKb())

	await state.update_data(message_ids=[msg.message_id])

	await callback.answer()


# ИМЕНИТЬ Д/З(ЧЕТВЕРТЫЙ УРОВЕНЬ)

@router.message(admStates.textHomework, F.text | F.photo)
async def enter_homework(message: Message, state: FSMContext):
	data = await state.get_data()
	subject = data.get("subject")
	date = data.get("current_date")

	message_ids = data.get("message_ids", [])
	message_ids.append(message.message_id)

	text = message.caption if message.photo else message.text
	photo_id = message.photo[-1].file_id if message.photo else None

	if not text and not photo_id:
		msg = await message.answer("⚠️ Пожалуйста, отправьте текст или фото с подписью!")
		message_ids.append(msg)

		return

	try:
		await addHomework(date, subject, text, photo_id) 
	except Exception as e:
		print(f"error: fail save homework\n{e}")
	
	await state.update_data(message_ids=message_ids)
	await delete_old_messages(message.chat.id, state)

	await state.set_state(admStates.homework)

	await adm_send_homework(message, state, date)




# РАССЫЛКА(ПЕРВЫЙ УРОВЕНЬ)

@router.callback_query(lambda callback: 'delete_message_' in callback.data, admStates.mailing)
async def deleteMailing(callback: CallbackQuery, state: FSMContext):
	msg_id = int(callback.data.split("_")[-1])
	await deleteMessage(msg_id)

	await adm_send_mailing(callback.message, state)


@router.callback_query(lambda c: c.data == "mailing", admStates.mailing)
async def startMailing(callback: CallbackQuery, state: FSMContext):
	messages = await getMailing()

	if not messages:
		await callback.answer("❌ Нет сообщений для рассылки")
		return

	users = await getAllUsers()

	for user in users:
		if user['id'] != callback.from_user.id:
			try:
				for message_id, (text, photo_id) in messages.items():
					if text and photo_id:
						await bot.send_photo(user['id'], photo_id, caption=text, parse_mode='HTML')
					elif text and not photo_id:
						await bot.send_message(user['id'], text, parse_mode='HTML')
					elif photo_id and not text:
						await bot.send_photo(user['id'], photo_id, parse_mode='HTML')

			except Exception as e:
				print(f"info: failed to send message to user {user['id']}\n{e}")

	await callback.answer("✅ Выполнено") 


@router.callback_query(lambda c: c.data == "add_message", admStates.mailing)
async def addMailing(callback: CallbackQuery, state: FSMContext):
	await state.set_state(admStates.addMail)

	await delete_old_messages(callback.message.chat.id, state)

	msg = await callback.message.answer("Отправьте сообщение которое хотите отправить", reply_markup=backKb())

	await state.update_data(message_ids=[msg.message_id])


# РАССЫЛКА(ВТОРОЙ УРОВЕНЬ)

@router.message(admStates.addMail)
async def addMailing2(message: Message, state: FSMContext):
	data = await state.get_data()
	message_ids = data.get("message_ids", [])
	message_ids.append(message.message_id)

	text = message.caption if message.caption else message.text
	photo_id = message.photo[-1].file_id if message.photo else None

	if not text and not photo_id:
		msg = await message.answer("❌ Отправьте текст или фото.")
		message_ids.append(msg.message_id)

		return

	await addMessage(text, photo_id)

	await state.set_state(admStates.mailing)
	await adm_send_mailing(message, state)


# ДОБАВИТЬ УЧАСТНИКА(ПЕРВЫЙ УРОВЕНЬ)

@router.callback_query(lambda callback: "add_user_" in callback.data, admStates.usersModify)
async def newPersonName(callback: CallbackQuery, state: FSMContext):
	await delete_old_messages(callback.message.chat.id, state)

	ID = int(callback.data.split('_')[-1])
	print("info: newPersonName")

	if not await inUnknowns(ID):
		await callback.answer("❌ Пользователя нет в списке")
		return

	await state.update_data(ID=ID)
	await state.set_state(admStates.enterName)

	msg = await callback.message.answer("Введите его имя и фамилию:", reply_markup=backKb())
	await state.update_data(message_ids=[msg.message_id])

@router.message(F.text == "🔙 Назад", admStates.chooseRole)
async def newPersonName(message: Message, state: FSMContext):
	data = await state.get_data()
	message_ids = data.get("message_ids", [])
	message_ids.append(message.message_id)

	await delete_old_messages(message.chat.id, state)

	print("info: newPersonName")

	await state.set_state(admStates.enterName)

	msg = await message.answer("Введите его имя и фамилию:", reply_markup=backKb())
	await state.update_data(message_ids=[msg.message_id])


# ДОБАВИТЬ УЧАСТНИКА(ВТОРОЙ УРОВЕНЬ)

@router.message(IsText(), admStates.enterName)
async def newPersonRole(message: Message, state: FSMContext):
	data = await state.get_data()
	message_ids = data.get("message_ids", [])
	message_ids.append(message.message_id)

	fullname = message.text
	await state.update_data(fullname=fullname)
	await state.set_state(admStates.chooseRole)
	msg = await message.answer("Выберете роль", reply_markup = chooseRoleKb())
	message_ids.append(msg.message_id)


# ДОБАВИТЬ УЧАСТНИКА(ТРЕТИЙ УРОВЕНЬ)

@router.message(F.text == '🔙 Назад', admStates.chooseRole)
async def newPersonRoleBack(message: Message, state: FSMContext):
	data = await state.get_data()
	message_ids = data.get("message_ids", [])
	message_ids.append(message.message_id)

	await state.set_state(admStates.enterName)
	msg = await message.answer("Введите его имя и фамилию", reply_markup=backKb())
	message_ids.append(msg.message_id)


@router.message(IsText(), admStates.chooseRole)
async def newPersonEnd(message: Message, state: FSMContext):
	data = await state.get_data()
	message_ids = data.get("message_ids", [])
	message_ids.append(message.message_id)

	print(f"info: {message.from_user.id} added new user")

	ROLE = message.text

	if not ROLE in ('Админ', 'Ученик'):
		msg = await message.answer("Введите корректную роль ⚠️ ")
		message_ids.append(msg.message_id)

		return

	data = await state.get_data()

	ID = data.get("ID")
	NAME = data.get("fullname")
	SMID = await getSMID(ID)

	if ROLE == 'Админ':
		await addUser(ID, NAME, 'admin')

	else:
		await addUser(ID, NAME)
	
	await bot.delete_message(ID, SMID)

	await deleteUnknown(ID)

	name = (await getUserByID(message.from_user.id))[1]

	if ROLE == "Ученик":
		await bot.send_message(ID, 
							   "<b>Дневник 10А Школы №17</b>\n\n📋 Главное меню", 
							   parse_mode='HTML',
							   reply_markup=menuKb())
	else:
		await bot.send_message(ID, 
							   "<b>Дневник 10А Школы №17</b>\n\n📋 Главное меню", 
							   parse_mode='HTML', 
							   reply_markup=admMenuKb())


	await state.set_state(admStates.admin)
	await adm_send_users(message, state)


# УДАЛИТЬ УЧАСТНИКА(ПЕРВЫЙ УРОВЕНЬ)

@router.callback_query(admStates.usersModify, lambda callback: "delete_user_" in callback.data)
async def deletePerson2(callback: CallbackQuery, state: FSMContext):

	ID = int(callback.data.split("_")[-1])

	user = await getUserByID(ID)

	await deleteUser(ID)
	
	if callback.from_user.id != ID:
		name = (await getUserByID(callback.from_user.id))[1]
	else:
		name = "Неизвестный"

	admins = await getAdminAndDeveloperIDs()
	for admin in admins:
		if not (admin == callback.from_user.id):
			await bot.send_message(admin, f"❌ {name} удалил(а) пользователя {user[1]}")

	await adm_send_users(callback.message, state)

