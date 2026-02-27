from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.booking import ManagerContactState
from keyboards.inline import main_menu_kb
from config import ADMIN_GROUP_ID
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.callback_query(F.data == "contact_manager")
async def ask_manager_question(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ManagerContactState.waiting_for_message)
    await callback.message.edit_text(
        "Напишите ваш вопрос или сообщение одним текстом. Мы передадим его менеджеру.",
        reply_markup=None
    )

@router.message(ManagerContactState.waiting_for_message)
async def forward_to_manager(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    text = f"Вопрос от @{username} (ID: {user_id}):\n\n{message.text}"
    
    try:
        await bot.send_message(chat_id=ADMIN_GROUP_ID, text=text)
        await message.answer(
            "Ваше сообщение успешно отправлено менеджеру. Мы ответим вам в ближайшее время!",
            reply_markup=main_menu_kb()
        )
    except Exception as e:
        logger.error(f"Failed to forward message to admin group: {e}")
        await message.answer(
            "Извините, произошла ошибка при отправке сообщения. Попробуйте еще раз позже.",
            reply_markup=main_menu_kb()
        )
    finally:
        await state.clear()

@router.message(
    F.chat.id == ADMIN_GROUP_ID,
    F.reply_to_message,
)
async def reply_from_manager(message: Message, bot: Bot):
    original_text = message.reply_to_message.text
    if not original_text or "(ID: " not in original_text:
        return
    
    try:
        start_idx = original_text.find("(ID: ") + 5
        end_idx = original_text.find(")", start_idx)
        user_id = int(original_text[start_idx:end_idx])
        
        reply_text = f"👨‍💻 <b>Ответ менеджера:</b>\n\n{message.text}"
        await bot.send_message(chat_id=user_id, text=reply_text, parse_mode="HTML")
        await message.reply("✅ Ответ успешно отправлен пользователю.")
    except Exception as e:
        logger.error(f"Failed to send reply to user: {e}")
        await message.reply("❌ Не удалось отправить ответ пользователю.")
