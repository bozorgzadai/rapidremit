from telegram import Update
from telegram.ext import ContextTypes
from create_keyboard import admin_menu_keyboard
from BotStates import AdminStates
from controller import get_admin_control



async def goto_admin_menu(update, context, message=None):
    default_message = "یک گزینه را انتخاب کنید:"

    if message:
        show_message = message
    else:
        show_message = default_message

    result = get_admin_control(update, context)
    if result:
        await update.message.reply_text(
            show_message,
            reply_markup=admin_menu_keyboard()
        )
        return AdminStates.ADMIN_MENU


async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "پیام همگانی":
        # from handlers.italy.italy_main import goto_italy
        # return await goto_italy(update)
        pass

    else:
        message = "لطفا یکی از گزینه‌های موجود را انتخاب کنید."
        return await goto_admin_menu(update, context, message)
    




