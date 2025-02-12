from telegram import Update
from telegram.ext import ContextTypes
from BotStates import States
from handlers.main_menu import goto_main_menu
from create_keyboard import italy_main_menu_keyboard



async def goto_italy(update, message=None):
    default_message = "لطفا یکی از گزینه‌های زیر را انتخاب کنید:"

    if message:
        show_message = message
    else:
        show_message = default_message

    await update.message.reply_text(
        show_message,
        reply_markup=italy_main_menu_keyboard()
    )
    return States.ITALY

async def italy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_main_menu(update, context)
    
    if text == "رزرو آزمون":
        from handlers.italy.exam.exam_main import goto_italy_reserve_exam
        return await goto_italy_reserve_exam(update)
    
    elif text == "پرداخت چیمه آ(CIMEA)":
        from handlers.italy.cimea import goto_italy_cimea
        return await goto_italy_cimea(update)
    
    elif text == "اپ فی":
        from handlers.italy.app_tuition_fee import goto_italy_app_fee_uni
        context.user_data["is_app_fee"] = True
        return await goto_italy_app_fee_uni(update)
    
    elif text == "شهریه دانشگاه":
        from handlers.italy.app_tuition_fee import goto_italy_app_fee_uni
        context.user_data["is_app_fee"] = False
        return await goto_italy_app_fee_uni(update)
    
    elif text == "رزرو هتل و هواپیما":
        from handlers.italy.reserve_hotel import goto_italy_reserve_hotel_id
        return await goto_italy_reserve_hotel_id(update)
    
    elif text == "ثبت نام دانشگاه":
        from handlers.italy.register_uni import goto_italy_register_university_name
        return await goto_italy_register_university_name(update)
    
    else:
        message = "لطفا یکی از گزینه‌های موجود را انتخاب کنید."
        return await goto_italy(update, message)












