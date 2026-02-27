from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Dict, Any

def main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="📅 Забронировать поездку", callback_data="book_trip"))
    builder.row(InlineKeyboardButton(text="❓ FAQ", callback_data="faq"))
    builder.row(InlineKeyboardButton(text="👨‍💻 Связаться с менеджером", callback_data="contact_manager"))
    return builder.as_markup()

def destinations_kb(destinations: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for dest in destinations:
        dest_id = dest.get('id')
        dest_name = dest.get('name', 'Unknown')
        builder.row(InlineKeyboardButton(text=dest_name, callback_data=f"dest_{dest_id}"))
    builder.row(InlineKeyboardButton(text="« Назад", callback_data="back_to_main"))
    return builder.as_markup()

def dates_kb(schedules: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for sch in schedules:
        sch_id = sch.get('id')
        sch_date = sch.get('date', 'Unknown date')
        builder.row(InlineKeyboardButton(text=sch_date, callback_data=f"date_{sch_id}"))
    builder.row(InlineKeyboardButton(text="« Назад", callback_data="book_trip"))
    return builder.as_markup()

def confirmation_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_booking"),
        InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_booking")
    )
    return builder.as_markup()
