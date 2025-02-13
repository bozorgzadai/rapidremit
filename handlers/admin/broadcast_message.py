from telegram import Update
from telegram.ext import ContextTypes
from BotStates import AdminStates
from handlers.admin.admin_menu import admin_menu,goto_admin_menu
from create_keyboard import back_button_keyboard
from controller import broadcast_message


async def goto_broacast(update, message=None):
    default_message = "لطفا متن مورد نظر را بنویسید:"

    if message:
        show_message = message
    else:
        show_message = default_message

    await update.message.reply_text(
        show_message,
        reply_markup=back_button_keyboard()
    )
    return AdminStates.BROADCAST

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await admin_menu(update, context)
    await broadcast_message(context,text)
    return await goto_admin_menu(update,context)
    
    











