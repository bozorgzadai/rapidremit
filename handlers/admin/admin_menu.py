from telegram import Update
from telegram.ext import ContextTypes
from create_keyboard import admin_menu_keyboard
from BotStates import AdminStates
from controller import get_admin_control, get_order_controller



async def goto_admin_menu(update, context, message=None):
    default_message = "یک گزینه را انتخاب کنید:"

    if message:
        show_message = message
    else:
        show_message = default_message

    is_admin = get_admin_control(update, context)
    if is_admin:
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
    elif text == "سفارش‌های تکمیل نشده":
        from handlers.admin.isfinish_order import goto_isfinish_order
        context.user_data["isfinish_order"] = get_order_controller(0)
        context.user_data["isfinish_bool"] = 0
        context.user_data["order_counter"] = 0
        context.user_data["isfinish_order_empty"] = "تمام سفارشات تکمیل شده‌اند."
        context.user_data["isfinish_order_keyboard"] = "تکمیل شود"
        context.user_data["isfinish_final_text"] = "به لیست تکمیل‌ها پیوست."
        return await goto_isfinish_order(update, context)
    
    elif text == "سفارش‌های تکمیل شده":
        from handlers.admin.isfinish_order import goto_isfinish_order
        context.user_data["isfinish_order"] = get_order_controller(1)
        context.user_data["isfinish_bool"] = 1
        context.user_data["order_counter"] = 0
        context.user_data["isfinish_order_empty"] = "هیچ سفارش تکمیل شده‌ای وجود ندارد."
        context.user_data["isfinish_order_keyboard"] = "لغو تکمیل"
        context.user_data["isfinish_final_text"] = "از لیست تکمیل شده‌ها حذف گردید."
        return await goto_isfinish_order(update, context)

    else:
        message = "لطفا یکی از گزینه‌های موجود را انتخاب کنید."
        return await goto_admin_menu(update, context, message)
    




