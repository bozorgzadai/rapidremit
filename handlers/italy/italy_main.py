from telegram import Update
from telegram.ext import ContextTypes
from handlers.States import States
from handler import goto_main_menu


from create_keyboard import (reply_keyboard_reg_type, reply_keyboard_reg_course_level, reply_keyboard_reg_course_lang,
                        reply_keyboard_tolc_exam_type, reply_keyboard_tolc_exam_detail, italy_main_menu_keyboard, reserve_exam_keyboard,
                        back_button_keyboard, pay_cancel_keyboard, yes_no_keyboard)

from controller import (get_id_by_regTypeName_control, get_id_by_regCourseLevelName_control, get_id_by_regCourseLangName_control,
                        reg_uni_control, get_id_by_tolcExamTypeName_control, get_id_by_tolcExamDetailName_control,
                        insert_or_update_cisia_account, tolc_order_exam_control, torvergata_control)




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
    











