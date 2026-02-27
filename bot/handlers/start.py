from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards.inline import main_menu_kb
from api_client import api_client
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    
    # Check if user exists, if not create
    user = await api_client.get_user(user_id)
    if not user:
        user_data = {
            "telegram_id": user_id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
        }
        await api_client.create_user(user_data)
        
    await message.answer(
        "Привет! Мы организуем комфортные визараны. Выбери действие:",
        reply_markup=main_menu_kb()
    )

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "Привет! Мы организуем комфортные визараны. Выбери действие:",
        reply_markup=main_menu_kb()
    )

@router.callback_query(F.data == "faq")
async def show_faq(callback: CallbackQuery):
    faq_text = (
        "❓ <b>Часто задаваемые вопросы:</b>\n\n"
        "1. Как проходит визаран?\n"
        "- Мы забираем вас, везем на границу, помогаем с оформлением документов и привозим обратно.\n\n"
        "2. Какие документы нужны?\n"
        "- Паспорт (срок действия не менее 6 месяцев)."
    )
    await callback.message.edit_text(faq_text, reply_markup=main_menu_kb(), parse_mode="HTML")
