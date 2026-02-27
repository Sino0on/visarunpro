from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.booking import BookingState
from keyboards.inline import destinations_kb, dates_kb, confirmation_kb, main_menu_kb
from api_client import api_client
import httpx

router = Router()

@router.callback_query(F.data == "book_trip")
async def start_booking(callback: CallbackQuery, state: FSMContext):
    destinations = await api_client.get_destinations()
    if not destinations:
        await callback.message.answer("К сожалению, сейчас нет доступных направлений. Попробуйте позже.")
        await callback.answer()
        return

    await state.set_state(BookingState.choosing_destination)
    await callback.message.edit_text(
        "Выберите направление:",
        reply_markup=destinations_kb(destinations)
    )

@router.callback_query(BookingState.choosing_destination, F.data.startswith("dest_"))
async def choose_date(callback: CallbackQuery, state: FSMContext):
    destination_id = int(callback.data.split("_")[1])
    await state.update_data(destination_id=destination_id)
    
    schedules = await api_client.get_schedule(destination_id)
    if not schedules:
        await callback.message.answer("К сожалению, на это направление сейчас нет доступных дат.")
        await callback.answer()
        return

    await state.set_state(BookingState.choosing_date)
    await callback.message.edit_text(
        "Выберите удобную дату:",
        reply_markup=dates_kb(schedules)
    )

@router.callback_query(BookingState.choosing_date, F.data.startswith("date_"))
async def ask_fullname(callback: CallbackQuery, state: FSMContext):
    schedule_id = int(callback.data.split("_")[1])
    await state.update_data(schedule_id=schedule_id)
    
    await state.set_state(BookingState.entering_fullname)
    await callback.message.edit_text("Пожалуйста, введите ваше ФИО:")

@router.message(BookingState.entering_fullname)
async def ask_phone(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await state.set_state(BookingState.entering_phone)
    await message.answer("Пожалуйста, введите ваш номер телефона:")

@router.message(BookingState.entering_phone)
async def confirm_booking_step(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    
    data = await state.get_data()
    text = (
        "Пожалуйста, проверьте данные бронирования:\n\n"
        f"👤 ФИО: {data.get('fullname')}\n"
        f"📞 Телефон: {data.get('phone')}\n\n"
        "Всё верно?"
    )
    
    await state.set_state(BookingState.confirming_booking)
    await message.answer(text, reply_markup=confirmation_kb())

@router.callback_query(BookingState.confirming_booking, F.data == "confirm_booking")
async def finish_booking(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    booking_data = {
        "user_id": callback.from_user.id,
        "schedule_id": data.get("schedule_id"),
        "fullname": data.get("fullname"),
        "phone": data.get("phone")
    }
    
    try:
        await api_client.create_booking(booking_data)
        await callback.message.edit_text(
            "✅ Ваша заявка успешно отправлена! Менеджер свяжется с вами в ближайшее время.",
            reply_markup=main_menu_kb()
        )
        await state.clear()
    except (httpx.TimeoutException, httpx.HTTPError):
        await callback.message.edit_text(
            "❌ Извините, сервис временно недоступен. Попробуйте немного позже.",
            reply_markup=main_menu_kb()
        )
        await state.clear()

@router.callback_query(BookingState.confirming_booking, F.data == "cancel_booking")
async def cancel_booking(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "Бронирование отменено. Выберите действие:",
        reply_markup=main_menu_kb()
    )
