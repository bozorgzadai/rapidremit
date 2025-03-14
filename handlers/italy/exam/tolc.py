from telegram import Update
from telegram.ext import ContextTypes
from BotStates import States
from handlers.main_menu import goto_main_menu
from utils import save_transaction_image
from handlers.italy.exam.exam_main import goto_italy_reserve_exam
from create_keyboard import (reply_keyboard_tolc_exam_type, reply_keyboard_tolc_exam_detail, back_button_keyboard,
                             pay_cancel_keyboard, yes_no_keyboard)

from controller import (get_id_by_tolcExamTypeName_control, get_id_by_tolcExamDetailName_control,
                        insert_or_update_cisia_account, tolc_order_exam_control)
from utils import get_euro_to_toman_exchange_rate_api, save_transaction_image



async def goto_italy_reserve_exam_tolc(update, message=None):
    default_message = "لطفا یکی از گزینه‌های زیر را انتخاب کنید:"

    if message:
        show_message = message
    else:
        show_message = default_message

    await update.message.reply_text(
        show_message,
        reply_markup=reply_keyboard_tolc_exam_type()
    )
    return States.ITALY_RESERVE_EXAM_TOLC

async def italy_reserve_exam_tolc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_italy_reserve_exam(update)
    
    elif text.startswith("TOLC-"):
        context.user_data["tolcExamTypeName"] = text
        context.user_data["tolcExamTypeId"] = get_id_by_tolcExamTypeName_control(text)

        message = f"لطفاً {text} را انتخاب کنید:"
        return await goto_italy_reserve_exam_tolc_x(update, context, message)
    else:
        message = "لطفا یکی از گزینه‌های موجود را انتخاب کنید."
        return await goto_italy_reserve_exam_tolc(update, message=None)




async def goto_italy_reserve_exam_tolc_x(update, context, message):
    await update.message.reply_text(
        message,
        reply_markup=reply_keyboard_tolc_exam_detail(context.user_data["tolcExamTypeId"])
    )
    return States.ITALY_RESERVE_EXAM_TOLC_X

async def handle_iolc_x_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_italy_reserve_exam_tolc(update)
    
    if text.startswith("ENGLISH TOLC-") or text.startswith("TOLC-"):
        context.user_data["tolcExamDetailId"] = get_id_by_tolcExamDetailName_control(text)
        return await goto_have_cisia_account(update)
    else:
        message = "لطفا یکی از گزینه‌های موجود را انتخاب کنید."
        return await goto_italy_reserve_exam_tolc_x(update, context, message)



async def goto_have_cisia_account(update, message=None):
    default_message = "آیا داخل سایت cisia دارای اکانت هستید؟"

    if message:
        show_message = message
    else:
        show_message = default_message

    await update.message.reply_text(
        show_message,
        reply_markup= yes_no_keyboard()
    )
    return States.HAVE_CISIA_ACCOUNT

async def have_cisia_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        x_full = context.user_data["tolcExamTypeName"]
        message = f"لطفاً {x_full} را انتخاب کنید:"
        return await goto_italy_reserve_exam_tolc_x(update, context, message)

    elif text == "بله":
        context.user_data["have_cisia_account"] = True
        return await goto_get_cisia_username(update)

    elif text == "خیر":
        context.user_data["have_cisia_account"] = False
        return await goto_get_exam_date(update)

    else:
        message = "لطفا یکی از گزینه‌های موجود را انتخاب کنید."
        return await goto_have_cisia_account(update, message)



async def goto_get_cisia_username(update):
    await update.message.reply_text(
        "لطفا نام کاربری سایت cisia خود را وارد کنید",
        reply_markup=back_button_keyboard()
    )
    return States.GET_CISIA_USERNAME

async def get_cisia_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_have_cisia_account(update)

    context.user_data["cisia_account_username"] = update.message.text
    return await goto_get_cisia_pass(update)



async def goto_get_cisia_pass(update):
    await update.message.reply_text(
        "لطفا رمز  سایت cisia خود را وارد کنید",
        reply_markup=back_button_keyboard()
    )
    return States.GET_CISIA_PASS

async def get_cisia_pass(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_get_cisia_username(update)

    context.user_data["cisia_account_password"] = update.message.text
    return await goto_get_exam_date(update)



async def goto_get_exam_date(update):
    await update.message.reply_text(
        "لطفا روز آزمون درخواستی را برای ما بنویسید",
        reply_markup=back_button_keyboard()
    )
    return States.GET_EXAM_DATE

async def get_exam_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        if context.user_data["have_cisia_account"]:
            return await goto_get_cisia_pass(update)
        else:
            return await goto_have_cisia_account(update)

    context.user_data["told_exam_date"] = update.message.text
    return await goto_get_id(update)



async def goto_get_id(update):
    await update.message.reply_text(
        "لطفا آیدی خود را وارد نمایید",
        reply_markup=back_button_keyboard()
    )
    return States.GET_ID

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_get_exam_date(update)

    context.user_data["id"] = update.message.text
    return await goto_get_phone(update)



async def goto_get_phone(update):
    await update.message.reply_text(
        "لطفا شماره تلفن خود را وارد نمایید",
        reply_markup=back_button_keyboard()
    )
    return States.GET_PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_get_id(update)

    context.user_data["contact"] = update.message.text
    return await goto_confirm_payment(update, context)



async def goto_confirm_payment(update, context, message=None):
    euro_amount = 35
    euro_price, unit = await get_euro_to_toman_exchange_rate_api()
    amount_rial = int(euro_amount  * euro_price + 480000)

    context.user_data["tolc_euro_amount"] = euro_amount
    context.user_data["tolc_euro_price"] = euro_price
    context.user_data["tolc_rial"] = amount_rial

    default_message = f"""داوطلب گرامی هزینه شرکت در آزمون  {amount_rial} تومان می‌باشد.\nاگر صحت اطلاعات خود و موجودی ظرفیت در روز درخواستی اطلاع دارید با استفاده از گزینه پرداخت درخواست خود را تکمیل کنید."""
    
    if message:
        show_message = message
    else:
        show_message = default_message
    
    await update.message.reply_text(
        show_message,
        reply_markup=pay_cancel_keyboard()
    )
    return States.CONFIRM_PAYMENT

async def confirm_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_get_phone(update)
    elif text == "پرداخت":
        return await goto_payment(update)
    elif text == "انصراف":
        return await goto_main_menu(update, context)
    else:
        message = "لطفا یکی از گزینه‌های موجود را انتخاب کنید."
        return await goto_confirm_payment(update, context, message)




async def goto_payment(update, message=None):
    card_number = "5022-2913-3054-7298\nنیما فتوکیان"

    default_message = f"""لطفا جهت پرداخت هزینه مبلغ مذکور را به شماره کارت\n {card_number}\n واریز نمایید.\n
سپس فیش پرداختی خود را در همین ربات ارسال کنید (عکس فیش را بفرستید)."""

    if message:
        show_message = message
    else:
        show_message = default_message

    await update.message.reply_text(
        show_message,
        reply_markup=back_button_keyboard()
    )
    return States.PAYMENT

async def payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.photo:
        save_directory = "saved_photo/tolc_exam"
        filename = await save_transaction_image(update, context, save_directory)
        context.user_data["tolc_exam_trans_filepath"] = filename

        tolc_order_exam_control(update, context)

        if context.user_data["have_cisia_account"]:
            insert_or_update_cisia_account(context)

        message = "کاربر گرامی درخواست شما با موفقیت ثبت شد. ادمین‌های پرداختی ما در سریع‌ترین فرصت با شما ارتباط خواهند گرفت."
        return await goto_main_menu(update, context, message)
    else:
        message = "لطفا یک عکس از فیش پرداختی خود ارسال کنید."
        return await goto_payment(update, message)
    
