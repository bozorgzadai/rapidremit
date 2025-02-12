from telegram import Update
from telegram.ext import ContextTypes
from BotStates import States
from handlers.main_menu import goto_main_menu
from handlers.italy.italy_main import goto_italy
from create_keyboard import reserve_exam_keyboard



async def goto_italy_reserve_exam(update, message=None):
    default_message = "لطفا نوع آزمون را انتخاب کنید:"

    if message:
        show_message = message
    else:
        show_message = default_message

    await update.message.reply_text(
        show_message,
        reply_markup=reserve_exam_keyboard()
    )
    return States.ITALY_RESERVE_EXAM

async def italy_reserve_exam(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_italy(update)
    
    elif text == "TOLC":
        from handlers.italy.exam.tolc import goto_italy_reserve_exam_tolc
        return await goto_italy_reserve_exam_tolc(update)
    
    elif text == "داروسازی تورورگاتا":
        from handlers.italy.exam.torvergata import goto_reserve_torvergata_id
        return await goto_reserve_torvergata_id(update)
    
    elif text in ["IMAT","TIL", "ARCHED"]:
        message = "اطلاعات آزمون درخواستی یافت نشد لطفا جهت اطلاعات بیشتر با پشتیبانی Rapid Remit به نشانی زیر ارتباط بگیرید \n @Rapidremit_support\n"
        return await goto_main_menu(update, context, message)
    
    else:
        message = "لطفا یکی از گزینه‌های موجود را انتخاب کنید."
        return await goto_italy_reserve_exam(update, message)
    