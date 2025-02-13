from telegram import Update
from telegram.ext import ContextTypes 
from create_keyboard import main_menu_keyboard
from BotStates import States
from controller import insert_or_update_user


async def goto_main_menu(update, context, message=None):
    default_message = "خوش آمدید! یک گزینه را انتخاب کنید:"
    insert_or_update_user(update, context)
    if message:
        show_message = message
    else:
        show_message = default_message

    await update.message.reply_text(
        show_message,
        reply_markup=main_menu_keyboard()
    )
    return States.MAIN_MENU

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "Italy":
        from handlers.italy.italy_main import goto_italy
        return await goto_italy(update)
    
    elif text == "خرید یورو":
        from handlers.buy_euro import goto_buy_euro
        return await goto_buy_euro(update)
    
    elif text == "موارد دیگر":
        from handlers.other_order import goto_others
        return await goto_others(update)
    
    elif text == "تکمیل سفارشات قبلی":
        print("Must Complete!")
    
    else:
        message = "لطفا یکی از گزینه‌های موجود را انتخاب کنید."
        return await goto_main_menu(update, context, message)

