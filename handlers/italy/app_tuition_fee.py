from telegram import Update
from telegram.ext import ContextTypes
from BotStates import States
from utils import get_euro_to_toman_exchange_rate_api, save_transaction_image
from handlers.main_menu import goto_main_menu
from handlers.italy.italy_main import goto_italy
from create_keyboard import back_button_keyboard, pay_cancel_keyboard
from controller import (app_fee_control, tuition_fee_control)



async def goto_italy_app_fee_uni(update):
    await update.message.reply_text(
        "کاربر گرامی لطفا نام دانشگاه درخواستی را وارد کنید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_APP_FEE_UNI

async def italy_app_fee_uni(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_italy(update)

    context.user_data["app_fee_university"] = text
    return await goto_italy_app_fee_degree(update)
    


async def goto_italy_app_fee_degree(update):
    await update.message.reply_text(
        "کاربر گرامی لطفا مقطع مورد نظر و رشته‌ی درخواستی را وارد کنید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_APP_FEE_DEGREE

async def italy_app_fee_degree(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_italy_app_fee_uni(update)

    context.user_data["app_fee_degree"] = text
    return await goto_italy_app_fee_tgid(update)
    


async def goto_italy_app_fee_tgid(update):
    await update.message.reply_text(
        "کاربر گرامی لطفا آیدی تلگرامی خود را جهت ارتباط‌های بعدی وارد نمایید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_APP_FEE_TGID

async def italy_app_fee_tgid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_italy_app_fee_degree(update)

    context.user_data["id"] = text
    return await goto_italy_app_fee_contact(update)
    



async def goto_italy_app_fee_contact(update):
    await update.message.reply_text(
        "کاربر گرامی لطفا شماره تماس خود را جهت پیگیری‌های آتی وارد نمایید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_APP_FEE_CONTACT

async def italy_app_fee_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_italy_app_fee_tgid(update)

    context.user_data["contact"] = text
    if context.user_data["is_app_fee"]:
            return await goto_italy_app_fee_amount(update)
    else:
        tuition_fee_control(update, context)

        message = """کاربر گرامی، درخواست شما با موفقیت ثبت شد. ادمین‌های پرداختی ما در سریع‌ترین فرصت با شما ارتباط خواهند گرفت."""
        return await goto_main_menu(update, context, message)
        
    
    
    

async def goto_italy_app_fee_amount(update, message=None):
    default_message = "لطفا مبلغ دقیق اپلیکشن فی کورس درخواستی خود را به یورو وارد کنید:"

    if message:
        show_message = message
    else:
        show_message = default_message

    await update.message.reply_text(
        show_message,
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_APP_FEE_AMOUNT

async def italy_app_fee_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    error_message = "لطفا یک مقدار معتبر به یورو وارد کنید."
    text = update.message.text

    if text == "بازگشت":
        return await goto_italy_app_fee_contact(update)
    
    elif text.isdigit():
        amount_eur = float(text)
        if amount_eur <= 0:
            return await goto_italy_app_fee_amount(update, error_message)

        context.user_data["app_fee_euro_amount"] = amount_eur
        euro_price, unit = await get_euro_to_toman_exchange_rate_api()
        context.user_data["app_fee_euro_price"] = euro_price
        amount_rial = int(amount_eur * 1.25 * euro_price)
        context.user_data["app_fee_rial"] = amount_rial

        return await goto_italy_app_fee_confirm(update, context)
    else:
        return await goto_italy_app_fee_amount(update, error_message)



async def goto_italy_app_fee_confirm(update, context, message=None):
    amount_rial = context.user_data["app_fee_rial"]
    default_message = f"""با توجه به اطلاعات وارده، هزینه‌ی درخواست جاری {amount_rial} ریال می‌باشد.\nجهت ادامه، یکی از گزینه‌های زیر را انتخاب کنید:"""
    if message:
        show_message = message
    else:
        show_message = default_message

    await update.message.reply_text(
        show_message,
        reply_markup=pay_cancel_keyboard()
    )
    return States.ITALY_APP_FEE_CONFIRM

async def italy_app_fee_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    amount_rial = context.user_data["app_fee_rial"]

    if text == "بازگشت":
        return await goto_italy_app_fee_amount(update)

    elif text == "پرداخت":
        return await goto_italy_app_fee_receipt(update, context)

    elif text == "انصراف":
        return await goto_main_menu(update, context)

    else:
        message = "گزینه نامعتبر. لطفا بازگشت، پرداخت یا انصراف را انتخاب کنید."
        return await goto_italy_app_fee_confirm(update, amount_rial, message)




async def goto_italy_app_fee_receipt(update, context, message=None):
    card_number = "5022-2913-3054-7298\nنیما فتوکیان"
    amount_rial = context.user_data["app_fee_rial"]

    default_message = f"""لطفا جهت پرداخت هزینه {amount_rial} تومان، مبلغ مذکور را به شماره کارت\n {card_number}\n واریز نمایید.\n
سپس فیش پرداختی خود را در همین ربات ارسال کنید (عکس فیش را بفرستید)."""

    if message:
        show_message = message
    else:
        show_message = default_message

    await update.message.reply_text(
        show_message,
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_APP_FEE_RECEIPT

async def italy_app_fee_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        return await goto_italy_app_fee_confirm(update, context, message=None)

    elif update.message.photo:
        save_directory = "saved_photo/app_and_tuition_fee"
        filename = await save_transaction_image(update, context, save_directory)
        context.user_data["app_fee_trans_filepath"] = filename

        if context.user_data["is_app_fee"]:
            app_fee_control(update, context)
        else:
            tuition_fee_control(update, context)

        message = """کاربر گرامی، درخواست شما با موفقیت ثبت شد. ادمین‌های پرداختی ما در سریع‌ترین فرصت با شما ارتباط خواهند گرفت."""
        return await goto_main_menu(update, context, message)
    else:
        message = "لطفا یک عکس از فیش پرداختی خود ارسال کنید."
        return await goto_italy_app_fee_receipt(update, context, message)

