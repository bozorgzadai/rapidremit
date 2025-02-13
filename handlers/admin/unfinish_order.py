from telegram import Update
from telegram.ext import ContextTypes
from create_keyboard import unfinish_order_keyboard
from BotStates import AdminStates
from controller import get_admin_control, update_finish_controller
from handlers.admin.admin_menu import goto_admin_menu
from utils import send_image, remove_lines_by_index
import os



async def goto_unfinish_order(update, context, message=None):
    is_admin = get_admin_control(update, context)
    if is_admin:
        if message:
            show_message = message
        else:
            unfinish_order = context.user_data["unfinish_order"]
            if len(unfinish_order) == 0:
                message = "تمام سفارشات تکمیل شده‌اند."
                return await goto_admin_menu(update, context, message)
            
            order_counter = context.user_data["order_counter"]
            if order_counter < 0:
                context.user_data["order_counter"] = 0
                show_message = "ابتدای لیست هستید!"
            elif order_counter == len(unfinish_order):
                context.user_data["order_counter"] = len(unfinish_order)-1
                show_message = "انتهای لیست هستید!"
            else:
                order = unfinish_order[order_counter]
                show_message = remove_lines_by_index(order[0])

                if order[1]:
                    image_path = os.path.join("saved_photo", order[2], order[1])
                    await send_image(update, context, image_path)

        await update.message.reply_text(
            show_message,
            reply_markup=unfinish_order_keyboard()
        )
        return AdminStates.UNFINISH_ORDER



async def unfinish_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        from handlers.admin.admin_menu import goto_admin_menu
        return await goto_admin_menu(update)
    
    elif text == "بعدی":
        context.user_data["order_counter"] += 1
        return await goto_unfinish_order(update, context)

    elif text == "قبلی":
        context.user_data["order_counter"] -= 1
        return await goto_unfinish_order(update, context)
    
    elif text == "تکمیل شود":
        unfinish_order = context.user_data["unfinish_order"]
        order_counter = context.user_data["order_counter"]
        order = unfinish_order[order_counter]
        update_finish_controller(order[0], 1)
        await update.message.reply_text("به لیست تکمیل‌ها پیوست.")

    else:
        message = "لطفا یکی از گزینه‌های موجود را انتخاب کنید."
        return await goto_unfinish_order(update, context, message)
    




