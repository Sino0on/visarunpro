from aiogram.fsm.state import State, StatesGroup

class BookingState(StatesGroup):
    choosing_destination = State()
    choosing_date = State()
    entering_fullname = State()
    entering_phone = State()
    confirming_booking = State()

class ManagerContactState(StatesGroup):
    waiting_for_message = State()
