from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import datetime


def admMenuKb():

	button1 = KeyboardButton(text="📅 Расписание")
	button2 = KeyboardButton(text="📝 Домашние задания")
	button3 = KeyboardButton(text="🛠️ Поддержка")
	button4 = KeyboardButton(text="🔒 Админка")

	kb = ReplyKeyboardMarkup(keyboard = [[button1],
						 [button2],
						 [button3],
						 [button4]],
				 resize_keyboard = True)

	return kb

def admAdmKb():

	button1 = KeyboardButton(text="📅 Изменить расписание")
	button2 = KeyboardButton(text="📝 Изменить Д/З")
	button3 = KeyboardButton(text="📢 Рассылка")
	button4 = KeyboardButton(text="👤 Изменить участников")
	back = KeyboardButton(text="🔙 Назад")

	kb = ReplyKeyboardMarkup(keyboard = [[button1],
						 [button2],
						 [button3],
						 [button4],
						 [back]],
				 resize_keyboard = True)

	return kb

def backKb():

	button1 = KeyboardButton(text="🔙 Назад")

	kb = ReplyKeyboardMarkup(keyboard = [[button1]],
				 resize_keyboard = True)

	return kb

def backIKb():

    back = InlineKeyboardButton(text="🔙 Назад", callback_data="back")
    ikb = InlineKeyboardMarkup(inline_keyboard=[[back]]) 

    return ikb

def chooseRoleKb():

	button1 = KeyboardButton(text="Ученик")
	button2 = KeyboardButton(text="Админ")
	button3 = KeyboardButton(text="🔙 Назад")

	kb = ReplyKeyboardMarkup(keyboard = [[button1],
						 [button2],
						 [button3]],
				 resize_keyboard = True)

	return kb

def deletePersonKb():

	button1 = KeyboardButton(text="Удалить")
	button2 = KeyboardButton(text="🔙 Назад")

	kb = ReplyKeyboardMarkup(keyboard = [[button1],
						 [button2]],
				 resize_keyboard = True)

	return kb

def deleteButtonIKb(ID: int):

	button = InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_message_{ID}")
	ikb = InlineKeyboardMarkup(inline_keyboard = [[button]])

	return ikb

def addUserButtonIKb(ID: int):

	button = InlineKeyboardButton(text="➕ Добавить", callback_data=f"add_user_{ID}")
	ikb = InlineKeyboardMarkup(inline_keyboard = [[button]])

	return ikb

def deleteUserButtonIKb(ID: int):

	button = InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_user_{ID}")
	ikb = InlineKeyboardMarkup(inline_keyboard = [[button]])

	return ikb

def mailingIKb():

	button1 = InlineKeyboardButton(text="Рассылка", callback_data="mailing")
	button2 = InlineKeyboardButton(text="Добавить сообщение", callback_data="add_message")

	kb = InlineKeyboardMarkup(inline_keyboard = [[button1],
						                         [button2]])

	return kb

def homeworkKb():

	button1 = KeyboardButton(text='Добавить')
	back = KeyboardButton(text='🔙 Назад')

	kb = ReplyKeyboardMarkup(keyboard = [[button1],
										 [back]],
							 resize_keyboard=True)

	return kb

def admWeekCalendarIkb(selected_date: datetime.date = None):

	if isinstance(selected_date, str):
		selected_date = datetime.date.fromisoformat(selected_date)

	if selected_date is None:
		selected_date = datetime.date.today()

	start_week = selected_date - datetime.timedelta(days=selected_date.weekday())

	days_map = {0: "Пн", 1: "Вт", 2: "Ср", 3: "Чт", 4: "Пт", 5: "Сб"}

	MONTHS_NOMINATIVE = [
			"январь", "февраль", "март", "апрель", "май", "июнь",
			"июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"
	]

	builder = InlineKeyboardBuilder()

	day_buttons = []
	for i in range(6):
		day = start_week + datetime.timedelta(days=i)
		button_text = f"{days_map.get(i, '')} {day.day:02d}"

		day_buttons.append(InlineKeyboardButton(text=button_text, callback_data=f"select_date:{day.isoformat()}"))

	builder.row(*day_buttons[0:3])
	builder.row(*day_buttons[3:6])

	prev_week = start_week - datetime.timedelta(days=7)
	next_week = start_week + datetime.timedelta(days=7)

	month_year_text = selected_date.strftime(f"{MONTHS_NOMINATIVE[start_week.month - 1]}")

	builder.row(
			InlineKeyboardButton(text="<<", callback_data=f"change_week:{prev_week.isoformat()}"),
			InlineKeyboardButton(text=month_year_text, callback_data="ignore"),
			InlineKeyboardButton(text=">>", callback_data=f"change_week:{next_week.isoformat()}")
	)

	builder.row(InlineKeyboardButton(text="➕ Добавить задание", callback_data="add_homework"))

	return builder.as_markup()

