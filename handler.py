from telegram import Update
from telegram.ext import ContextTypes 

import os
import time
from api import get_euro_to_toman_exchange_rate
from controller import (app_fee_control, tuition_fee_control,
                        get_id_by_regTypeName_control, get_id_by_regCourseLevelName_control, get_id_by_regCourseLangName_control,
                        reg_uni_control, get_id_by_tolcExamTypeName_control, get_id_by_tolcExamDetailName_control,
                        insert_or_update_cisia_account, tolc_order_exam_control, torvergata_control, get_id_by_cimeaTypeName_control,
                        get_id_by_cimeaSpeedName_control, get_cimeaPrice_by_cimeaTypeAndSpeedId_control, cimea_control)
from create_keyboard import (reply_keyboard_reg_type, reply_keyboard_reg_course_level, reply_keyboard_reg_course_lang,
                        reply_keyboard_tolc_exam_type, reply_keyboard_tolc_exam_detail, reply_keyboard_cimea_type,
                        reply_keyboard_cimea_speed)

from create_keyboard import (main_menu_keyboard, italy_main_menu_keyboard, reserve_exam_keyboard,
                        back_button_keyboard, pay_cancel_keyboard, yes_no_keyboard)
from handlers.States import States








async def goto_main_menu(update, context, message=None):
    default_message = "خوش آمدید! یک گزینه را انتخاب کنید:"

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
        pass
    
    else:
        message = "لطفا یکی از گزینه‌های موجود را انتخاب کنید."
        return await goto_main_menu(update, context, message)
    




