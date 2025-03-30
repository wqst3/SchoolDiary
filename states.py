from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
	student = State()

	homework = State()

	message_ids = State()
	current_date = State()

	support = State()

class admStates(StatesGroup):
	admin = State()

	timetable = State()

	homework = State()
	dateHomework = State()
	subjectHomework = State()
	textHomework = State()

	mailing = State()
	addMail = State()
	startMailing = State()

	usersModify = State()

	newPerson = State()
	enterName = State()
	chooseRole = State()

	deletePerson = State()
	exactlyDeletePerson = State()

