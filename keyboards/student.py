from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import datetime


def menuKb():
	kb = ReplyKeyboardMarkup(keyboard=[
		[KeyboardButton(text="📅 Расписание")],
		[KeyboardButton(text="📝 Домашние задания")],
		[KeyboardButton(text="🛠️ Поддержка")]], 
		resize_keyboard = True)

	return kb


def homeworkKb():

	back = KeyboardButton(text='Назад')

	kb = ReplyKeyboardMarkup(keyboard = [[back]],
							 resize_keyboard = True)

	return kb

def homeworkIKb(selected_date: datetime.date = None):

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

	return builder.as_markup()

def subjectIKb():

	builder = InlineKeyboardBuilder()

	builder.button(text="➗ Алгебра", callback_data="subject:Алгебра")
	builder.button(text="📐 Геометрия", callback_data="subject:Геометрия")
	builder.button(text="💻 Информатика", callback_data="subject:Информатика")

	builder.button(text="📜 История", callback_data="subject:История")
	builder.button(text="🤝 Обществознание", callback_data="subject:Обществознание")
	builder.button(text="📖 Литература", callback_data="subject:Литература")
	builder.button(text="🇷🇺 Русский язык", callback_data="subject:Русский язык")
	builder.button(text="🇬🇧 Английский язык", callback_data="subject:Английский язык")

	builder.button(text="⚛️ Физика", callback_data="subject:Физика")
	builder.button(text="🧪 Химия", callback_data="subject:Химия")
	builder.button(text="🌱 Биология", callback_data="subject:Биология")
	builder.button(text="🌍 География", callback_data="subject:География")

	builder.button(text="🚑 ОБЖ", callback_data="subject:ОБЖ")
	builder.button(text="🏛️ ИП", callback_data="subject:ИП")
	builder.button(text="⚙️ ВиС", callback_data="subject:ВиС")
	builder.button(text="🏃 Физкультура", callback_data="subject:Физкультура")

	builder.button(text="🔙 Назад", callback_data="back")

	builder.adjust(2)

	return builder.as_markup()

