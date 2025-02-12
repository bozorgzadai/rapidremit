from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes 

import os
from api import get_euro_to_toman_exchange_rate
from controller import (app_fee_control, tuition_fee_control,
                        get_id_by_regTypeName_control, get_id_by_regCourseLevelName_control, get_id_by_regCourseLangName_control,
                        reg_uni_control, get_id_by_tolcExamTypeName_control, get_id_by_tolcExamDetailName_control,
                        insert_or_update_cisia_account, tolc_order_exam_control, torvergata_control, get_id_by_cimeaTypeName_control,
                        get_id_by_cimeaSpeedName_control, get_cimeaPrice_by_cimeaTypeAndSpeedId_control, cimea_control)
import time
from create_keyboard import (reply_keyboard_reg_type, reply_keyboard_reg_course_level, reply_keyboard_reg_course_lang,
                        reply_keyboard_tolc_exam_type, reply_keyboard_tolc_exam_detail, reply_keyboard_cimea_type,
                        reply_keyboard_cimea_speed)

from create_keyboard import (main_menu_keyboard, italy_main_menu_keyboard, reserve_exam_keyboard,
                        back_button_keyboard, pay_cancel_keyboard, yes_no_keyboard)
from handlers.States import States



async def save_transaction_photo(update, context, save_directory):
    # Get the largest version of the photo (last item in the list)
    photo_file = await update.message.photo[-1].get_file()

    os.makedirs(save_directory, exist_ok=True)

    # Generate a unique file name using timestamp and user ID
    user_id = context._user_id  # Get the Telegram user ID
    # user_id = update.message.from_user.id  # Get the Telegram user ID
    timestamp = int(time.time() * 1000)  # Current time in milliseconds
    unique_filename = f"{user_id}_{timestamp}.jpg"

    # Define the path where you want to save the photo
    file_path = os.path.join(save_directory, unique_filename)

    # Download and save the photo
    await photo_file.download_to_drive(custom_path=file_path)

    return unique_filename




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
        return await goto_italy(update)
    
    elif text == "خرید یورو":
        from handlers.buy_euro import goto_buy_euro
        return await goto_buy_euro(update)
    
    elif text == "موارد دیگر":
        from handlers.other_order import goto_others
        return await goto_others(update)
    
    elif text == "تکمیل سفارشات قبلی":
        return await goto_complete_prev_orther(update)
    
    else:
        message = "لطفا یکی از گزینه‌های موجود را انتخاب کنید."
        return await goto_main_menu(update, context, message)
    






async def goto_complete_prev_orther(update):
    await update.message.reply_text(
        "لطفا شماره سفارشی را که از ادمین های پرداختی دریافت کرده اید را وارد کنید:",
        reply_markup=back_button_keyboard()
    )
    return States.TAKMIL_ORDER_NUMBER









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
        return await goto_italy_reserve_exam(update)
    elif text == "پرداخت چیمه آ(CIMEA)":
        return await goto_italy_cimea(update)
    elif text == "اپ فی":
        context.user_data["is_app_fee"] = True
        return await goto_italy_app_fee_uni(update)
    elif text == "شهریه دانشگاه":
        context.user_data["is_app_fee"] = False
        return await goto_italy_app_fee_uni(update)
    elif text == "رزرو هتل و هواپیما":
        return await goto_italy_reserve_hotel_id(update, context)
    elif text == "ثبت نام دانشگاه":
        return await goto_italy_register_university_name(update)
    else:
        message = "لطفا یکی از گزینه‌های موجود را انتخاب کنید."
        return await goto_italy(update, message)



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
        return await goto_italy_reserve_exam_tolc(update)
    elif text == "داروسازی تورورگاتا":
        return await goto_reserve_torvergata_id(update)
    elif text in ["IMAT","TIL", "ARCHED"]:
        message = "اطلاعات آزمون درخواستی یافت نشد لطفا جهت اطلاعات بیشتر با پشتیبانی Rapid Remit به نشانی زیر ارتباط بگیرید \n @Rapidremit_support\n"
        return await goto_main_menu(update, context, message)
    else:
        message = "لطفا یکی از گزینه‌های موجود را انتخاب کنید."
        return await goto_italy_reserve_exam(update, message)



async def goto_reserve_torvergata_id(update):
    await update.message.reply_text(
        "لطفا آیدی خود را وارد نمایید",
        reply_markup=back_button_keyboard()
    )
    return States.torvergata_ID

async def reserve_torvergata_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_italy_reserve_exam(update)

    context.user_data["id"] = text
    return await goto_reserve_torvergata_contact(update)
    


async def goto_reserve_torvergata_contact(update):
    await update.message.reply_text(
        "لطفا شماره تلفن خود را جهت ارتباطات بعدی وارد کنید:",
        reply_markup=back_button_keyboard()
    )
    return States.torvergata_CONTACT

async def reserve_torvergata_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_reserve_torvergata_id(update)
    
    context.user_data["contact"] = text
    return await goto_reserve_torvergata(update)

    

async def goto_reserve_torvergata(update, message=None):
    default_message = "داوطلب گرامی هزینه شرکت در آزمون داروسازی تورورگاتا (کورس انگلیسی داروسازی) 1000 ریال می‌باشد اگر قصد تکمیل خرید خود را دارید با استفاده از گزینه پرداخت ادامه دهید"

    if message:
        show_message = message
    else:
        show_message = default_message

    await update.message.reply_text(
        show_message,
        reply_markup=pay_cancel_keyboard()
    )
    return States.torvergata

async def reserve_torvergata(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_reserve_torvergata_contact(update)
    elif text == "انصراف":
        return await goto_main_menu(update, context)
    elif text == "پرداخت":
        return await goto_handle_payment_receipt(update)
    else: 
        message = "لطفا یکی از گزینه‌های زیر را انتخاب کنید:"
        return await goto_reserve_torvergata(update, message)



async def goto_handle_payment_receipt(update, message=None):
    default_message = "لطفا هزینه درخواست جاری خود را به شماره کارت 1234-5678-9012-3456 واریز نمایید و فیش پرداختی خود را در ربات ارسال نمایید."

    if message:
        show_message = message
    else:
        show_message = default_message

    await update.message.reply_text(
        show_message,
        reply_markup=back_button_keyboard()
    )
    return States.WAITING_FOR_PAYMENT

async def handle_payment_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.photo:
        save_directory = "saved_photo/torvergata"
        filename = await save_transaction_photo(update, context, save_directory)
        context.user_data["torvergata_trans_filepath"] = filename

        torvergata_control(update, context)

        message = "کاربر گرامی، درخواست شما با موفقیت ثبت شد. ادمین‌های پرداختی ما در سریع‌ترین فرصت با شما ارتباط خواهند گرفت."
        return await goto_main_menu(update, context, message)
    elif update.message.text=="بازگشت":
        return await goto_reserve_torvergata(update)
    else:
        message = "لطفا یک تصویر از فیش پرداختی خود ارسال کنید."
        return await goto_handle_payment_receipt(update, message)









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
    return await goto_confirm_payment(update)



async def goto_confirm_payment(update, message=None):
    exam_fee = "1000000"  # هزینه به تومان
    default_message = f"""داوطلب گرامی هزینه شرکت در آزمون فلان {exam_fee} تومان می‌باشد.\n
        اگر صحت اطلاعات خود و موجودی ظرفیت در روز درخواستی اطلاع دارید با استفاده از گزینه پرداخت درخواست خود را تکمیل کنید.
        """
    
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
        return await goto_confirm_payment(update, message)




async def goto_payment(update, message=None):
    default_message = "لطفا هزینه درخواست جاری خود را به شماره کارت فلان واریز نمایید و فیش پرداختی خود را در ربات ارسال نمایید"

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
        filename = await save_transaction_photo(update, context, save_directory)
        context.user_data["tolc_exam_trans_filepath"] = filename

        tolc_order_exam_control(update, context)

        if context.user_data["have_cisia_account"]:
            insert_or_update_cisia_account(context)

        message = "کاربر گرامی درخواست شما با موفقیت ثبت شد. ادمین‌های پرداختی ما در سریع‌ترین فرصت با شما ارتباط خواهند گرفت."
        return await goto_main_menu(update, context, message)
    else:
        message = "لطفا یک عکس از فیش پرداختی خود ارسال کنید."
        return await goto_payment(update, message)
    




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
    return await goto_italy_app_fee_amount(update)
    
    

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
        euro_price, unit = await get_euro_to_toman_exchange_rate()
        context.user_data["app_fee_euro_price"] = euro_price
        amount_rial = int(amount_eur * euro_price * 10)
        context.user_data["app_fee_rial"] = amount_rial

        return await goto_italy_app_fee_confirm(update, context)
    else:
        return await goto_italy_app_fee_amount(update, error_message)



async def goto_italy_app_fee_confirm(update, context, message=None):
    amount_rial = context.user_data["app_fee_rial"]
    default_message = f"""
                        با توجه به اطلاعات وارده، هزینه‌ی درخواست جاری {amount_rial} ریال می‌باشد.\n
                            جهت ادامه، یکی از گزینه‌های زیر را انتخاب کنید:
                        """
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
    card_number = "9876-5432-1098-7654"
    amount_rial = context.user_data["app_fee_rial"]

    default_message = f"""لطفا جهت پرداخت هزینه {amount_rial} ریال، مبلغ مذکور را به شماره کارت {card_number} واریز نمایید.\n
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
        filename = await save_transaction_photo(update, context, save_directory)
        context.user_data["app_fee_trans_filepath"] = filename

        if context.user_data["is_app_fee"]:
            app_fee_control(update, context)
        else:
            tuition_fee_control(update, context)

        message = """کاربر گرامی، درخواست شما با موفقیت ثبت شد. 
            ادمین‌های پرداختی ما در سریع‌ترین فرصت با شما ارتباط خواهند گرفت."""
        return await goto_main_menu(update, context, message)
    else:
        message = "لطفا یک عکس از فیش پرداختی خود ارسال کنید."
        return await goto_italy_app_fee_receipt(update, context, message)





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





async def goto_italy_reserve_hotel_id(update: Update) -> int:
    await update.message.reply_text(
        "کاربر گرامی لطفا آیدی تلگرامی خود را جهت ارتباط ادمین های پرداختی وارد نمایید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_RESERVE_HOTEL_ID

async def italy_reserve_hotel_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        return await goto_italy(update)

    context.user_data["id"] = update.message.text
    return await goto_italy_reserve_hotel_contact(update)
    


async def goto_italy_reserve_hotel_contact(update):
    await update.message.reply_text(
        "کاربر گرامی لطفا شماره تماس خود را جهت پیگیری های آتی برای سفارش خود وارد کنید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_RESERVE_HOTEL_CONTACT

async def italy_reserve_hotel_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        return await goto_italy_reserve_hotel_id(update, context)

    context.user_data["contact"] = update.message.text
    message = "ادمین های پرداختی جهت دریافت اطلاعات بیشتر از شما در راستای تکمیل سفارش ارتباط خواهند گرفت."
    return await goto_main_menu(update, context, message)
