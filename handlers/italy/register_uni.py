from telegram import Update
from telegram.ext import ContextTypes
from BotStates import States
from handlers.main_menu import goto_main_menu
from handlers.italy.italy_main import goto_italy
from create_keyboard import (back_button_keyboard, reply_keyboard_reg_type, reply_keyboard_reg_course_level,
                             reply_keyboard_reg_course_lang)
from controller import (get_id_by_regTypeName_control, get_id_by_regCourseLevelName_control, reg_uni_control,
                        get_id_by_regCourseLangName_control)



async def goto_italy_register_university_name(update: Update) -> int:
    await update.message.reply_text(
        "لطفا نام دانشگاه مدنظر که میخواهید پروسه Enrollment/apply را برای آن آغاز کنید وارد نمایید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_REGISTER_UNIVERSITY_NAME

async def italy_register_university_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        return await goto_italy(update)
    
    context.user_data["university_name"] = update.message.text
    return await goto_italy_register_university_type(update)
    



async def goto_italy_register_university_type(update):
    await update.message.reply_text(
        "لطفا نوع درخواست خود را مشخص کنید:",
        reply_markup=reply_keyboard_reg_type()
    )
    return States.ITALY_REGISTER_UNIVERSITY_TYPE

async def italy_register_university_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        return await goto_italy_register_university_name(update)

    context.user_data["university_type"] = get_id_by_regTypeName_control(update.message.text)
    return await goto_italy_register_university_course(update)
    


async def goto_italy_register_university_course(update):
    await update.message.reply_text(
        "لطفا نام کورس را انتخاب کنید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_REGISTER_UNIVERSITY_COURSE

async def italy_register_university_course(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        return await goto_italy_register_university_type(update)
    
    context.user_data["course_name"] = update.message.text
    return await goto_italy_register_university_degree(update)
    


async def goto_italy_register_university_degree(update):
    await update.message.reply_text(
        "لطفا مقطع کورس خود را انتخاب کنید:",
        reply_markup=reply_keyboard_reg_course_level()
    )
    return States.ITALY_REGISTER_UNIVERSITY_DEGREE

async def italy_register_university_degree(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        return await goto_italy_register_university_course(update)
    
    context.user_data["course_level"] = get_id_by_regCourseLevelName_control(update.message.text)
    return await goto_italy_register_university_language(update)
    


async def goto_italy_register_university_language(update):
    await update.message.reply_text(
        "لطفا زبان کورس خود را انتخاب کنید:",
        reply_markup=reply_keyboard_reg_course_lang()
    )
    return States.ITALY_REGISTER_UNIVERSITY_LANGUAGE

async def italy_register_university_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        return await goto_italy_register_university_degree(update)
    
    context.user_data["course_lang"] = get_id_by_regCourseLangName_control(update.message.text)
    return await goto_italy_register_university_tgid(update)
    


async def goto_italy_register_university_tgid(update):
    await update.message.reply_text(
        "لطفا آیدی تلگرامی خود را وارد نمایید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_REGISTER_UNIVERSITY_TGID

async def italy_register_university_tgid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        return await goto_italy_register_university_language(update)
    
    context.user_data["id"] = update.message.text
    return await goto_italy_register_university_contact(update)
    


async def goto_italy_register_university_contact(update):
    await update.message.reply_text(
        "لطفا شماره تماس خود را وارد کنید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_REGISTER_UNIVERSITY_CONTACT

async def italy_register_university_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        return await goto_italy_register_university_tgid(update)

    context.user_data["contact"] = update.message.text
    reg_uni_control(update, context)

    Message = "ادمین های پرداختی جهت دریافت اطلاعات بیشتر از شما در راستای تکمیل سفارش ارتباط خواهند گرفت."
    return await goto_main_menu(update, context, Message)
