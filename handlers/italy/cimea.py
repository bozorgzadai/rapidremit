from telegram import Update
from telegram.ext import ContextTypes
from handlers.States import States
from utils import save_transaction_photo
from handler import goto_main_menu
from handlers.italy.italy_main import goto_italy
from create_keyboard import back_button_keyboard, reply_keyboard_cimea_type, reply_keyboard_cimea_speed, pay_cancel_keyboard
from controller import (cimea_control, get_id_by_cimeaTypeName_control, get_id_by_cimeaSpeedName_control,
                        get_cimeaPrice_by_cimeaTypeAndSpeedId_control)



async def goto_italy_cimea(update: Update) -> int:
    await update.message.reply_text(
        "کاربر گرامی لطفا از بین گزینه های زیر نوع درخواست خود را مشخص کنید." 
        "(اگر برای دیپلم ثبت درخواست گواهی چیمه آ دارید صرفا میتوانید ثبت درخواست comparability کنید)",
        reply_markup=reply_keyboard_cimea_type()
    )
    return States.ITALY_CIMEA

async def italy_cimea(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_italy(update)
    
    context.user_data["cimea_type_id"] = get_id_by_cimeaTypeName_control(text)
    return await goto_italy_cimea_speed(update)

    


async def goto_italy_cimea_speed(update):
    await update.message.reply_text(
        "کاربر گرامی لطفا از بین گزینه های زیر نوع درخواست خود را مشخص کنید."
        "(درخواست عادی در بازه زمانی دوماهه و درخواست فوری در بازه زمانی یک ماهه قابل بررسی است)",
        reply_markup=reply_keyboard_cimea_speed()
    )
    return States.ITALY_CIMEA_SPEED

async def italy_cimea_speed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_italy_cimea(update)
    
    context.user_data["cimea_speed_id"] = get_id_by_cimeaSpeedName_control(text)
    cimeaTypeId = context.user_data["cimea_type_id"]
    cimeaSpeedId = context.user_data["cimea_speed_id"]
    cimeaPriceId, cimeaPrice = get_cimeaPrice_by_cimeaTypeAndSpeedId_control(cimeaTypeId, cimeaSpeedId)

    context.user_data["cimea_price_id"] = cimeaPriceId
    context.user_data["cimea_price"] = cimeaPrice
    return await goto_italy_cimea_confirm(update, context)
    
    


async def goto_italy_cimea_confirm(update, context, message=None):
    price = context.user_data["cimea_price"]
    default_message = f"با توجه به اطلاعات وارده هزینه درخواست جاری {price} ریال می‌باشد. آیا مایل به ادامه ی درخواست خود هستید؟"

    if message:
        show_message = message
    else:
        show_message = default_message

    await update.message.reply_text(
        show_message,
        reply_markup=pay_cancel_keyboard()
    )
    return States.ITALY_CIMEA_CONFIRM


async def italy_cimea_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_italy_cimea_speed(update)
    elif text == "انصراف":
        return await goto_main_menu(update, context)
    elif text == "پرداخت":
        return await goto_italy_cimea_receive_tg_id(update)
    else:
        message = "لطفا از بین گزینه‌های موجود یک مورد را انتخاب کنید"
        return await goto_italy_cimea_confirm(update, context, message)




async def goto_italy_cimea_receive_tg_id(update):
    await update.message.reply_text(
        "لطفا آیدی تلگرام خود را وارد کنید.",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_CIMEA_RECEIPT_ID

async def italy_cimea_receive_tg_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_italy_cimea_confirm(update, context)

    context.user_data["id"] = text
    return await goto_italy_cimea_receive_phone(update)
    



async def goto_italy_cimea_receive_phone(update):
    await update.message.reply_text(
        "لطفا شماره تماس خود را وارد کنید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_CIMEA_RECEIPT_PHONE

async def italy_cimea_receive_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_italy_cimea_receive_tg_id(update)

    context.user_data["contact"] = text
    return await goto_italy_cimea_receipt(update, context)




async def goto_italy_cimea_receipt(update, context, message=None):
    price = context.user_data["cimea_price"]
    default_message = f"لطفا جهت پرداخت درخواست جاری به مبلغ {price} ریال، هزینه مذکور را به شماره کارت 1234-5678-9012-3456 واریز نمایید و فیش پرداختی خود را در ربات ارسال نمایید."

    if message:
        show_message = message
    else:
        show_message = default_message

    await update.message.reply_text(
        show_message,
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_CIMEA_RECEIPT


async def italy_cimea_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.photo:
        save_directory = "saved_photo/cimea"
        filename = await save_transaction_photo(update, context, save_directory)
        context.user_data["cimea_trans_filepath"] = filename

        cimea_control(update, context)

        message = "کاربر گرامی درخواست شما با موفقیت ثبت شد. ادمین‌های پرداختی ما در سریع‌ترین فرصت با شما ارتباط خواهند گرفت."
        return await goto_main_menu(update, context, message)
    else:
        message = "لطفا یک تصویر از فیش پرداختی خود ارسال کنید."
        return await goto_italy_cimea_receipt(update, context, message)

