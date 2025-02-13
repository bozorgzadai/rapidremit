from telegram import Update
from telegram.ext import ContextTypes
from create_keyboard import isfinish_order_keyboard
from BotStates import AdminStates
from controller import get_admin_control, update_isfinish_controller
from handlers.admin.admin_menu import goto_admin_menu
from utils import send_image, remove_lines_by_index
import os



async def goto_isfinish_order(update, context, message=None):
    is_admin = get_admin_control(update, context)
    if is_admin:
        if message:
            show_message = message
        else:
            isfinish_order = context.user_data["isfinish_order"]
            if len(isfinish_order) == 0:
                message = context.user_data["isfinish_order_empty"]
                return await goto_admin_menu(update, context, message)
            
            order_counter = context.user_data["order_counter"]
            if order_counter < 0:
                context.user_data["order_counter"] = 0
                show_message = "ابتدای لیست هستید!"
            elif order_counter == len(isfinish_order):
                context.user_data["order_counter"] = len(isfinish_order)-1
                show_message = "انتهای لیست هستید!"
            else:
                order = isfinish_order[order_counter]
                show_message = remove_lines_by_index(order[0])

                if order[1]:
                    image_path = os.path.join("saved_photo", order[2], order[1])
                    await send_image(update, context, image_path)

        await update.message.reply_text(
            show_message,
            reply_markup=isfinish_order_keyboard(context.user_data["isfinish_order_keyboard"])
        )
        return AdminStates.ISFINISH_ORDER



async def isfinish_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        from handlers.admin.admin_menu import goto_admin_menu
        return await goto_admin_menu(update, context)
    
    elif text == "بعدی":
        context.user_data["order_counter"] += 1
        return await goto_isfinish_order(update, context)

    elif text == "قبلی":
        context.user_data["order_counter"] -= 1
        return await goto_isfinish_order(update, context)
    
    elif text == context.user_data["isfinish_order_keyboard"]:
        isfinish_order = context.user_data["isfinish_order"]
        order_counter = context.user_data["order_counter"]
        order = isfinish_order[order_counter]
        update_isfinish_controller(order[0], 1-context.user_data["isfinish_bool"])
        del isfinish_order[order_counter]
        context.user_data["order_counter"] -= 1
        await update.message.reply_text(context.user_data["isfinish_final_text"])

    else:
        message = "لطفا یکی از گزینه‌های موجود را انتخاب کنید."
        return await goto_isfinish_order(update, context, message)
    




