from enum import Enum, auto
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)
from config import TOKEN

import os
from api import get_euro_to_toman_exchange_rate
from controller import (buy_euro_control, other_order_control, app_fee_control, tuition_fee_control,
                        get_id_by_regTypeName_control, get_id_by_regCourseLevelName_control, get_id_by_regCourseLangName_control,
                        reg_uni_control, get_id_by_tolcExamTypeName_control, get_id_by_tolcExamDetailName_control)
import time
from create_btn import (reply_keyboard_reg_type, reply_keyboard_reg_course_level, reply_keyboard_reg_course_lang,
                        reply_keyboard_tolc_exam_type, reply_keyboard_tolc_exam_detail)

class States(Enum):
    MAIN_MENU = auto()
    BUY_EURO_AMOUNT = auto()
    BUY_EURO_CONTACT = auto()
    BUY_EURO_ID = auto()
    OTHERS_DESCRIPTION = auto()
    OTHERS_AMOUNT = auto()
    OTHERS_CONTACT = auto()
    OTHERS_ID = auto()
    ITALY_MAIN_MENU = auto()
    ITALY_RESERVE_EXAM = auto()
    ITALY_RESERVE_EXAM_TOLC = auto()
    ITALY_RESERVE_EXAM_TOLC_X = auto()
    ITALY_CIMEA_PAYMENT = auto()
    ITALY_CIMEA_TYPE = auto()
    ITALY_CIMEA_SPEED = auto()
    ITALY_CIMEA_CONFIRM = auto()
    ITALY_CIMEA_RECEIPT = auto()
    ITALY_APP_FEE = auto()
    ITALY_RESERVE_HOTEL = auto()
    ITALY_REGISTER_UNIVERSITY = auto()
    TAKMIL_ORDER_NUMBER = auto()
    TAKMIL_AMOUNT = auto()
    TAKMIL_RECEIPT = auto()
    TORMAGATA = auto()
    TORMAGATA_ID = auto()
    TORMAGATA_CONTACT = auto()

    ITALY_RESERVE_EXAM_CISIA_ACCOUNT = auto()  # بررسی اکانت CISIA
    ITALY_RESERVE_EXAM_DATE = auto()  # وارد کردن روز آزمون
    ITALY_RESERVE_EXAM_TGID = auto()  # وارد کردن آیدی تلگرام
    ITALY_RESERVE_EXAM_PHONE = auto()  # وارد کردن شماره تلفن
    ITALY_RESERVE_EXAM_PAYMENT = auto()  # تایید پرداخت
    ITALY_RESERVE_EXAM_RECEIPT = auto()  # دریافت فیش پرداخت

    
    # حالات جدید مربوط به اپ فی
    ITALY_APP_FEE_UNI = auto()
    ITALY_APP_FEE_DEGREE = auto()
    ITALY_APP_FEE_TGID = auto()
    ITALY_APP_FEE_CONTACT = auto()
    ITALY_APP_FEE_AMOUNT = auto()
    ITALY_APP_FEE_CONFIRM = auto()
    ITALY_APP_FEE_RECEIPT = auto()
    
    # اضافه کردن حالت جدید برای مدیریت فیش پرداخت
    WAITING_FOR_PAYMENT = auto()

    ITALY_RESERVE_HOTEL_TGID = auto()  # وارد کردن آیدی تلگرام برای رزرو هتل و هواپیما
    ITALY_RESERVE_HOTEL_CONTACT = auto()  # وارد کردن شماره تماس برای رزرو هتل و هواپیما

    # حالات جدید برای ثبت نام دانشگاه
    ITALY_REGISTER_UNIVERSITY_NAME = auto()  # وارد کردن نام دانشگاه
    ITALY_REGISTER_UNIVERSITY_TYPE = auto()  # انتخاب نوع درخواست (apply/enrollment)
    ITALY_REGISTER_UNIVERSITY_COURSE = auto()  # انتخاب نام کورس
    ITALY_REGISTER_UNIVERSITY_DEGREE = auto()  # انتخاب مقطع کورس
    ITALY_REGISTER_UNIVERSITY_LANGUAGE = auto()  # انتخاب زبان کورس
    ITALY_REGISTER_UNIVERSITY_TGID = auto()  # وارد کردن آیدی تلگرام
    ITALY_REGISTER_UNIVERSITY_CONTACT = auto()  # وارد کردن شماره تماس

    ITALY_CIMEA_RECEIPT_ID = auto()
    ITALY_CIMEA_RECEIPT_PHONE = auto()

    ITALY_RESERVE_EXAM_TOLC_PASS2 = auto()
    ITALY_RESERVE_EXAM_TOLC_PASS = auto()


    MINE_MENU = auto()
    GET_CISIA_USERNAME = auto()
    GET_CISIA_PASS = auto()
    GET_EXAM_DATE = auto()
    GET_ID = auto()
    GET_PHONE = auto()
    CONFIRM_PAYMENT = auto()
    PAYMENT = auto()


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

    return file_path


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    buy_euro_btn = KeyboardButton("خرید یورو")
    italy_btn = KeyboardButton("Italy")
    others_btn = KeyboardButton("Others")
    takmil_btn = KeyboardButton("تکمیل سفارشات قبلی")
    return ReplyKeyboardMarkup(
        [
            [italy_btn],
            [buy_euro_btn, others_btn],
            [takmil_btn],
        ],
        resize_keyboard=True,
    )

def back_button_keyboard() -> ReplyKeyboardMarkup:
    back_btn = KeyboardButton("بازگشت")
    return ReplyKeyboardMarkup(
        [
            [back_btn],
        ],
        resize_keyboard=True,
    )

def italy_main_menu_keyboard() -> ReplyKeyboardMarkup:
    reserve_exam_btn = KeyboardButton("رزرو آزمون")
    cimea_payment_btn = KeyboardButton("پرداخت چیمه آ(CIMEA)")
    app_fee_btn = KeyboardButton("اپ فی")
    uni_tui_btn = KeyboardButton("شهریه دانشگاه")
    reserve_hotel_btn = KeyboardButton("رزرو هتل و هواپیما")
    register_university_btn = KeyboardButton("ثبت نام دانشگاه")
    back_btn = KeyboardButton("بازگشت")
    return ReplyKeyboardMarkup(
        [
            [reserve_exam_btn],
            [cimea_payment_btn],
            [app_fee_btn, uni_tui_btn],
            [register_university_btn, reserve_hotel_btn],
            [back_btn]
        ],
        resize_keyboard=True,
    )

def reserve_exam_keyboard() -> ReplyKeyboardMarkup:
    tolc_btn = KeyboardButton("TOLC")
    imai_btn = KeyboardButton("IMAT")
    drg_btn = KeyboardButton("داروسازی تورورگاتا")
    til_btn = KeyboardButton("TIL")
    arcd_btn = KeyboardButton("ARCHED")
    back_btn = KeyboardButton("بازگشت")
    return ReplyKeyboardMarkup(
        [
            [tolc_btn],
            [imai_btn, drg_btn],
            [til_btn, arcd_btn],
            [back_btn]
        ],
        resize_keyboard=True,
    )

# def reply_keyboard_tolc_exam_type() -> ReplyKeyboardMarkup:
#     tolc_i_btn = KeyboardButton("TOLC-I")
#     tolc_f_btn = KeyboardButton("TOLC-F")
#     tolc_e_btn = KeyboardButton("TOLC-E")
#     tolc_s_btn = KeyboardButton("TOLC-S")
#     tolc_su_btn = KeyboardButton("TOLC-SU")
#     tolc_b_btn = KeyboardButton("TOLC-B")
#     tolc_av_btn = KeyboardButton("TOLC-AV")
#     tolc_psi_btn = KeyboardButton("TOLC-PSi")
#     tolc_sb_btn = KeyboardButton("TOLC-SB")
#     tolc_lp_btn = KeyboardButton("TOLC-LP")
#     back_btn = KeyboardButton("بازگشت")
#     return ReplyKeyboardMarkup(
#         [
#             [tolc_i_btn, tolc_f_btn],
#             [tolc_e_btn, tolc_s_btn],
#             [tolc_su_btn, tolc_b_btn],
#             [tolc_av_btn, tolc_psi_btn],
#             [tolc_sb_btn, tolc_lp_btn],
#             [back_btn],
#         ],
#         resize_keyboard=True,
#     )

# def tolc_x_keyboard(x_suffix: str) -> ReplyKeyboardMarkup:
#     english_btn = KeyboardButton(f"ENGLISH TOLC-{x_suffix}")
#     iolc_btn = KeyboardButton(f"TOLC-{x_suffix}")
#     back_btn = KeyboardButton("بازگشت")
#     return ReplyKeyboardMarkup(
#         [
#             [english_btn, iolc_btn],
#             [back_btn],
#         ],
#         resize_keyboard=True,
#     )

def tormagata_keyboard() -> ReplyKeyboardMarkup:
    pay_btn = KeyboardButton("پرداخت")
    cancel_btn = KeyboardButton("انصراف")
    return ReplyKeyboardMarkup(
        [
            [cancel_btn, pay_btn],
        ],
        resize_keyboard=True,
    )

def app_fee_confirm_keyboard() -> ReplyKeyboardMarkup:
    pay_btn = KeyboardButton("پرداخت")
    cancel_btn = KeyboardButton("انصراف")
    return ReplyKeyboardMarkup(
        [
            [pay_btn, cancel_btn],
        ],
        resize_keyboard=True,
    )

def enseraf_menu() -> ReplyKeyboardMarkup:
    cancel_btn = KeyboardButton("انصراف")
    return ReplyKeyboardMarkup(
        [
            [cancel_btn],
        ],
        resize_keyboard=True,
    )

# --- هندلرها ---

# هندلر دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Welcome! Choose an option:",
        reply_markup=main_menu_keyboard()
    )
    return States.MAIN_MENU

# هندلر انتخاب منوی اصلی
async def main_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("main")
    text = update.message.text
    if text == "خرید یورو":
        await update.message.reply_text(
            "لطفا مبلغی که نیاز به ترانسفر آن به حساب بانکی خود دارید به یورو وارد نمایید:",
            reply_markup=back_button_keyboard()
        )
        return States.BUY_EURO_AMOUNT
    elif text == "Others":
        await update.message.reply_text(
            "لطفا توضیحات سفارش خود را وارد کنید:",
            reply_markup=back_button_keyboard()
        )
        return States.OTHERS_DESCRIPTION
    elif text == "Italy":
        await update.message.reply_text(
            "لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=italy_main_menu_keyboard()
        )
        return States.ITALY_MAIN_MENU
    elif text == "تکمیل سفارشات قبلی":
        await update.message.reply_text(
            "لطفا شماره سفارشی را که از ادمین های پرداختی دریافت کرده اید را وارد کنید:",
            reply_markup=back_button_keyboard()
        )
        return States.TAKMIL_ORDER_NUMBER
    else:
        await update.message.reply_text(
            "لطفا یکی از گزینه‌های موجود را انتخاب کنید.",
            reply_markup=main_menu_keyboard()
        )
        return States.MAIN_MENU

# هندلر خرید یورو - دریافت مبلغ
async def buy_euro_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        await update.message.reply_text(
            "Welcome! Choose an option:",
            reply_markup=main_menu_keyboard()
        )
        return States.MAIN_MENU
    if text.isdigit():
        context.user_data["amount"] = float(text)
        await update.message.reply_text(
            "لطفا شماره خود را جهت ارتباطات بعدی وارد کنید:",
            reply_markup=back_button_keyboard()
        )
        return States.BUY_EURO_CONTACT
    else:
        await update.message.reply_text(
            "لطفا یک عدد معتبر وارد کنید.",
            reply_markup=back_button_keyboard()
        )
        return States.BUY_EURO_AMOUNT

# هندلر خرید یورو - دریافت اطلاعات تماس
async def buy_euro_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        await update.message.reply_text(
            "لطفا مبلغی که نیاز به ترانسفر آن به حساب بانکی خود دارید به یورو وارد نمایید:",
            reply_markup=back_button_keyboard()
        )
        return States.BUY_EURO_AMOUNT
    context.user_data["contact"] = text
    # پردازش داده‌ها یا ارسال به ادمین
    await update.message.reply_text(
        "لطفا آیدی خود را وارد کنید",
        reply_markup=back_button_keyboard()
    )
    return States.BUY_EURO_ID

async def buy_euro_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        await update.message.reply_text(
            "لطفا مبلغی که نیاز به ترانسفر آن به حساب بانکی خود دارید به یورو وارد نمایید:",
            reply_markup=back_button_keyboard()
        )
        return States.BUY_EURO_AMOUNT
    context.user_data["id"] = text
    # پردازش داده‌ها یا ارسال به ادمین
    await update.message.reply_text(
        "ادمین‌های پرداختی حوزه خرید یورو و تبدیل ارز در سریع‌ترین حالت با شما جهت اقدامات تکمیلی ارتباط خواهند گرفت.",
        reply_markup=main_menu_keyboard()
    )
    buy_euro_control(update, context)
    return States.MAIN_MENU


# هندلر سفارشات دیگر - دریافت توضیحات
async def others_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        await update.message.reply_text(
            "Welcome! Choose an option:",
            reply_markup=main_menu_keyboard()
        )
        return States.MAIN_MENU
    context.user_data["description"] = text
    await update.message.reply_text(
        "لطفا مبلغ قابل پرداخت در سفارش را به یورو وارد کنید:",
        reply_markup=back_button_keyboard()
    )
    return States.OTHERS_AMOUNT

# هندلر سفارشات دیگر - دریافت مبلغ
async def others_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        await update.message.reply_text(
            "لطفا توضیحات سفارش خود را وارد کنید:",
            reply_markup=back_button_keyboard()
        )
        return States.OTHERS_DESCRIPTION
    if text.isdigit():
        context.user_data["amount"] = float(text)
        await update.message.reply_text(
            "لطفا شماره تماس خود را وارد کنید:",
            reply_markup=back_button_keyboard()
        )
        return States.OTHERS_CONTACT
    else:
        await update.message.reply_text(
            "لطفا یک عدد معتبر وارد کنید.",
            reply_markup=back_button_keyboard()
        )
        return States.OTHERS_AMOUNT

# هندلر سفارشات دیگر - دریافت اطلاعات تماس
async def others_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        await update.message.reply_text(
            "لطفا مبلغ قابل پرداخت در سفارش را وارد کنید:",
            reply_markup=back_button_keyboard()
        )
        return States.OTHERS_AMOUNT
    context.user_data["contact"] = text
    # پردازش داده‌ها یا ارسال به ادمین
    await update.message.reply_text(
        "لطفا آیدی خود را وارد نمایید",
        reply_markup=back_button_keyboard()
    )
    return States.OTHERS_ID

async def others_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        await update.message.reply_text(
            "لطفا مبلغ قابل پرداخت در سفارش را وارد کنید:",
            reply_markup=back_button_keyboard()
        )
        return States.OTHERS_AMOUNT
    context.user_data["id"] = text
    # پردازش داده‌ها یا ارسال به ادمین
    await update.message.reply_text(
        "سفارش شما ثبت شد. ادمین به زودی با شما تماس خواهد گرفت.",
        reply_markup=main_menu_keyboard()
    )
    other_order_control(update, context)
    return States.MAIN_MENU

# هندلر منوی Italy
async def italy_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "رزرو آزمون":
        await update.message.reply_text(
            "لطفا نوع آزمون را انتخاب کنید:",
            reply_markup=reserve_exam_keyboard()
        )
        return States.ITALY_RESERVE_EXAM

    elif text == "بازگشت":
        await update.message.reply_text(
            "Welcome! Choose an option:",
            reply_markup=main_menu_keyboard()
        )
        return States.MAIN_MENU

    elif text == "پرداخت چیمه آ(CIMEA)":
        return await italy_cimea_payment(update, context)

    elif text == "اپ فی":
        context.user_data["is_app_fee"] = True
        # وقتی کاربر اپ فی را می‌زند، وارد مرحله نخست اپ فی شویم
        return await italy_app_fee(update, context)

    elif text == "شهریه دانشگاه":
        context.user_data["is_app_fee"] = False
        # می‌خواهیم از همین منطق اپ فی استفاده کنیم
        return await italy_app_fee(update, context)

    elif text == "رزرو هتل و هواپیما":
        return await italy_reserve_hotel(update, context)

    elif text == "ثبت نام دانشگاه":
        return await italy_register_university(update, context)

    else:
        await update.message.reply_text(
            "لطفا یکی از گزینه‌های موجود را انتخاب کنید.",
            reply_markup=italy_main_menu_keyboard()
        )
        return States.ITALY_MAIN_MENU

# هندلر انتخاب رزرو آزمون در Italy
async def italy_reserve_exam(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        await update.message.reply_text(
            "لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=italy_main_menu_keyboard()
        )
        return States.ITALY_MAIN_MENU
    elif text == "TOLC":
        await update.message.reply_text(
            "لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=reply_keyboard_tolc_exam_type()
        )
        return States.ITALY_RESERVE_EXAM_TOLC
    elif text == "داروسازی تورورگاتا":
        await update.message.reply_text(
            "لطفا آیدی خود را وارد نمایید",
            reply_markup=back_button_keyboard()
        )
        return States.TORMAGATA_ID

        
    elif text in ["IMAT","TIL", "ARCHED"]:
        await update.message.reply_text(
            f"اطلاعات آزمون درخواستی یافت نشد لطفا جهت اطلاعات بیشتر با پشتیبانی Rapid Remit به نشانی زیر ارتباط بگیرید \n @Rapidremit_support\n",
            reply_markup=main_menu_keyboard()
        )
        return States.MAIN_MENU
    else:
        await update.message.reply_text(
            "لطفا یکی از گزینه‌های موجود را انتخاب کنید.",
            reply_markup=reserve_exam_keyboard()
        )
        return States.ITALY_RESERVE_EXAM


async def reserve_tormagata_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        await update.message.reply_text(
            "لطفا یکی از گزینه های زیر را انتخاب نمایید",
            reply_markup=italy_main_menu_keyboard()
        )
        return States.ITALY_MAIN_MENU
    else:
        context.user_data["amount"] = text
        await update.message.reply_text(
            "لطفا شماره تلفن خود را جهت ارتباطات بعدی وارد کنید:",
            reply_markup=back_button_keyboard()
        )
        return States.TORMAGATA_CONTACT


# هندلر خرید یورو - دریافت اطلاعات تماس
async def reserve_tormagata_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        await update.message.reply_text(
            "لطفا شماره تلفن خود را وارد نمایید:",
            reply_markup=back_button_keyboard()
        )
        return States.TORMAGATA_ID
    context.user_data["contact"] = text
    # پردازش داده‌ها یا ارسال به ادمین
    await update.message.reply_text(
            "داوطلب گرامی هزینه شرکت در آزمون داروسازی تورورگاتا (کورس انگلیسی داروسازی) 1000 ریال می‌باشد اگر قصد تکمیل خرید خود را دارید با استفاده از گزینه پرداخت ادامه دهید",
            reply_markup=tormagata_keyboard()
        )
    return States.TORMAGATA


# هندلر پرداخت آزمون تورموگاتا
async def reserve_tormagata(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "انصراف":
        await update.message.reply_text(
            "لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=main_menu_keyboard()
        )
        return States.MAIN_MENU
    elif text == "پرداخت":
        await update.message.reply_text(
            "لطفا هزینه درخواست جاری خود را به شماره کارت 1234-5678-9012-3456 واریز نمایید و فیش پرداختی خود را در ربات ارسال نمایید.",
            reply_markup=enseraf_menu()
        )
        return States.WAITING_FOR_PAYMENT
    else: 
        await update.message.reply_text(
            "لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=tormagata_keyboard()
        )
        return States.TORMAGATA

# هندلر دریافت فیش پرداخت (عکس) یا متن اشتباه
async def handle_payment_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.photo:
        await update.message.reply_text(
            "کاربر گرامی، درخواست شما با موفقیت ثبت شد. ادمین‌های پرداختی ما در سریع‌ترین فرصت با شما ارتباط خواهند گرفت.",
            reply_markup=main_menu_keyboard()
        )
        return States.MAIN_MENU
    elif update.message.text=="انصراف":
        await update.message.reply_text(
            "لطفا یکی از گزینه ها را انتخاب کنید.",
            reply_markup=main_menu_keyboard()
        )
        return States.MAIN_MENU
    else:
        await update.message.reply_text("لطفا یک تصویر از فیش پرداختی خود ارسال کنید.")
        return States.WAITING_FOR_PAYMENT









async def goto_italy_reserve_exam_tolc_x(update, context, message):
    await update.message.reply_text(
        message,
        reply_markup=reply_keyboard_tolc_exam_detail(context.user_data["tolcExamTypeId"])
    )
    return States.ITALY_RESERVE_EXAM_TOLC_X





# هندلر انتخاب نوع آزمون TOLC در Italy
async def italy_reserve_exam_tolc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        await update.message.reply_text(
            "لطفا نوع آزمون را انتخاب کنید:",
            reply_markup=reserve_exam_keyboard()
        )
        return States.ITALY_RESERVE_EXAM
    if text.startswith("TOLC-"):
        context.user_data["tolcExamTypeName"] = text
        context.user_data["tolcExamTypeId"] = get_id_by_tolcExamTypeName_control(text)

        message = f"لطفاً {text} را انتخاب کنید:"
        return await goto_italy_reserve_exam_tolc_x(update, context, message)
        # await update.message.reply_text(
        #     f"لطفاً {text} را انتخاب کنید:",
        #     reply_markup=tolc_x_keyboard(x_suffix)
        # )
        # return States.ITALY_RESERVE_EXAM_TOLC_X
    else:
        await update.message.reply_text(
            "لطفا یکی از گزینه‌های موجود را انتخاب کنید.",
            reply_markup=reply_keyboard_tolc_exam_type()
        )
        return States.ITALY_RESERVE_EXAM_TOLC



# هندلر انتخاب ENGLISH TOLC-X یا TOLC-X در Italy
async def handle_iolc_x_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        await update.message.reply_text(
            "لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=reply_keyboard_tolc_exam_type()
        )
        return States.ITALY_RESERVE_EXAM_TOLC
    
    if text.startswith("ENGLISH TOLC-") or text.startswith("TOLC-"):
        context.user_data["tolcExamDetailId"] = get_id_by_tolcExamDetailName_control(text)
        return await goto_mine_menu(update)
        # نمایش سوال مربوط به داشتن اکانت در سایت CISIA
        # await update.message.reply_text(
        #     "آیا داخل سایت cisia دارای اکانت هستید؟",
        #     reply_markup=ReplyKeyboardMarkup(
        #         [
        #             [KeyboardButton("بله"), KeyboardButton("خیر")],
        #             [KeyboardButton("بازگشت")]
        #         ],
        #         resize_keyboard=True,
        #     )
        # )
        # # return States.ITALY_RESERVE_EXAM_CISIA_ACCOUNT
        # return States.MINE_MENU

    else:
        message = "لطفا یکی از گزینه‌های موجود را انتخاب کنید."
        return await goto_italy_reserve_exam_tolc_x(update, context, message)
        # await update.message.reply_text(
        #     "لطفا یکی از گزینه‌های موجود را انتخاب کنید.",
        #     reply_markup=tolc_x_keyboard(x_suffix)
        # )
        # return States.ITALY_RESERVE_EXAM_TOLC_X




async def goto_main_menu(update, message):
    await update.message.reply_text(
        message,
        reply_markup=main_menu_keyboard()
    )
    return States.MAIN_MENU



async def goto_mine_menu(update, message="آیا داخل سایت cisia دارای اکانت هستید؟"):
    await update.message.reply_text(
        message,
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("بله"), KeyboardButton("خیر")],
                [KeyboardButton("بازگشت")]
            ],
            resize_keyboard=True,
        )
    )
    # return States.ITALY_RESERVE_EXAM_CISIA_ACCOUNT
    return States.MINE_MENU

async def mine_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        x_full = context.user_data.get("tolcExamTypeName", "8")
        message = f"لطفاً {x_full} را انتخاب کنید:"
        return await goto_italy_reserve_exam_tolc_x(update, context, message)
        # await update.message.reply_text(
        #     f"لطفاً {x_full} را انتخاب کنید:",
        #     reply_markup=tolc_x_keyboard(x_suffix)
        # )
        # return States.ITALY_RESERVE_EXAM_TOLC_X

    elif text == "بله":
        context.user_data["have_cisia_account"] = True
        return await goto_get_cisia_username(update)

    elif text == "خیر":
        context.user_data["have_cisia_account"] = False
        return await goto_get_exam_date(update)

    else:
        message = "لطفا یکی از گزینه‌های موجود را انتخاب کنید."
        return await goto_mine_menu(update, message)



async def goto_get_cisia_username(update):
    await update.message.reply_text(
        "لطفا نام کاربری سایت cisia خود را وارد کنید",
        reply_markup=back_button_keyboard()
    )
    return States.GET_CISIA_USERNAME

async def get_cisia_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_mine_menu(update)

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
            return await goto_mine_menu(update)

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
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("پرداخت"), KeyboardButton("انصراف")],
                [KeyboardButton("بازگشت")],
            ],
            resize_keyboard=True
        )
    )
    return States.CONFIRM_PAYMENT

async def confirm_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_get_phone(update)
    elif text == "پرداخت":
        return await goto_payment(update)
    elif text == "انصراف":
        return await goto_main_menu(update)
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
        file_path = await save_transaction_photo(update, context, save_directory)
        context.user_data["tolc_exam_trans_filepath"] = file_path

        message = "کاربر گرامی درخواست شما با موفقیت ثبت شد. ادمین‌های پرداختی ما در سریع‌ترین فرصت با شما ارتباط خواهند گرفت."
        return await goto_main_menu(update, message)
    else:
        message = "لطفا یک عکس از فیش پرداختی خود ارسال کنید."
        return await goto_payment(update, message)
    






async def cisia_account_yes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        await update.message.reply_text(
            "لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=reply_keyboard_tolc_exam_type()
        )
        return States.ITALY_RESERVE_EXAM_TOLC
    
    if text == "بله":
        # از کاربر نام کاربری و رمز عبور درخواست شود
        await update.message.reply_text(
            "لطفا نام کاربری سایت cisia خود را وارد کنید",
            reply_markup=back_button_keyboard()
        )
        return States.ITALY_RESERVE_EXAM_TOLC_PASS

async def cisia_account_yes_pass(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        await update.message.reply_text(
            "لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=reply_keyboard_tolc_exam_type()
        )
        return States.ITALY_RESERVE_EXAM_TOLC
    
        # از کاربر نام کاربری و رمز عبور درخواست شود
    await update.message.reply_text(
        "لطفا رمز  سایت cisia خود را وارد کنید",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_RESERVE_EXAM_TOLC_PASS2

async def cisia_account_yes_pass2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    await update.message.reply_text(
        "لطفا روز آزمون درخواستی را برای ما بنویسید",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_RESERVE_EXAM_DATE


async def handle_cisia_account_no(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        await update.message.reply_text(
            "لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=reply_keyboard_tolc_exam_type()
        )
        return States.ITALY_RESERVE_EXAM_TOLC

    # اگر کاربر "خیر" را انتخاب کند
    await update.message.reply_text(
        "لطفا روز آزمون درخواستی را برای ما بنویسید",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_RESERVE_EXAM_DATE

async def handle_exam_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        await update.message.reply_text(
            "لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=reply_keyboard_tolc_exam_type()
        )
        return States.ITALY_RESERVE_EXAM_TOLC

    context.user_data["exam_date"] = update.message.text
    await update.message.reply_text(
        "لطفا آیدی خود را وارد نمایید",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_RESERVE_EXAM_TGID


async def handle_telegram_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        await update.message.reply_text(
        "لطفا روز آزمون درخواستی را برای ما بنویسید",
        reply_markup=back_button_keyboard()
        )
        return States.ITALY_RESERVE_EXAM_DATE


    context.user_data["id"] = update.message.text
    await update.message.reply_text(
        "لطفا شماره تلفن خود را وارد نمایید",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_RESERVE_EXAM_PHONE


async def handle_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        await update.message.reply_text(
        "لطفا روز آزمون درخواستی را برای ما بنویسید",
        reply_markup=back_button_keyboard()
        )
        return States.ITALY_RESERVE_EXAM_DATE

    context.user_data["phone_number"] = update.message.text
    exam_fee = "1000000"  # هزینه به تومان
    await update.message.reply_text(
        f"داوطلب گرامی هزینه شرکت در آزمون فلان {exam_fee} تومان می‌باشد.\n"
        "اگر صحت اطلاعات خود و موجودی ظرفیت در روز درخواستی اطلاع دارید با استفاده از گزینه پرداخت درخواست خود را تکمیل کنید.",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("پرداخت"), KeyboardButton("انصراف")],
            ],
            resize_keyboard=True
        )
    )
    return States.ITALY_RESERVE_EXAM_PAYMENT

async def handle_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if update.message.text == "پرداخت":
        # ارسال شماره کارت
        await update.message.reply_text(
            "لطفا هزینه درخواست جاری خود را به شماره کارت فلان واریز نمایید و فیش پرداختی خود را در ربات ارسال نمایید",
            reply_markup=back_button_keyboard()
        )
        return States.ITALY_RESERVE_EXAM_RECEIPT
    elif update.message.text == "انصراف":
        # بازگشت به منوی اصلی
        await update.message.reply_text(
            "عملیات لغو شد",
            reply_markup=main_menu_keyboard()
        )
        return States.MAIN_MENU

async def handle_payment_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.photo:
        await update.message.reply_text(
            "کاربر گرامی درخواست شما با موفقیت ثبت شد. ادمین‌های پرداختی ما در سریع‌ترین فرصت با شما ارتباط خواهند گرفت.",
            reply_markup=main_menu_keyboard()
        )
        return States.MAIN_MENU
    else:
        await update.message.reply_text("لطفا یک عکس از فیش پرداختی خود ارسال کنید.")
        return States.ITALY_RESERVE_EXAM_RECEIPT






# هندلر اپ فی (قبلاً وجود داشت؛ اکنون پیاده‌سازی شده)
async def italy_app_fee(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    با انتخاب منوی 'اپ فی' یا 'شهریه دانشگاه'، کاربر وارد این تابع می‌شود.
    در این مرحله، ابتدا از کاربر نام دانشگاه درخواست می‌شود.
    """
    await update.message.reply_text(
        "کاربر گرامی لطفا نام دانشگاه درخواستی را وارد کنید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_APP_FEE_UNI

# مراحل بعدی اپ فی: گرفتن اطلاعات مختلف
async def italy_app_fee_university(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    مرحله وارد کردن نام دانشگاه
    """
    text = update.message.text
    if text == "بازگشت":
        # بازگشت به منوی اصلی Italy
        await update.message.reply_text(
            "لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=italy_main_menu_keyboard()
        )
        return States.ITALY_MAIN_MENU

    # ذخیره نام دانشگاه
    context.user_data["app_fee_university"] = text

    # مرحله بعد
    await update.message.reply_text(
        "کاربر گرامی لطفا مقطع مورد نظر و رشته‌ی درخواستی را وارد کنید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_APP_FEE_DEGREE

async def italy_app_fee_degree(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    مرحله وارد کردن مقطع و رشته
    """
    text = update.message.text
    if text == "بازگشت":
        # بازگشت به مرحله قبلی (وارد کردن نام دانشگاه)
        await update.message.reply_text(
            "کاربر گرامی لطفا نام دانشگاه درخواستی را وارد کنید:",
            reply_markup=back_button_keyboard()
        )
        return States.ITALY_APP_FEE_UNI

    context.user_data["app_fee_degree"] = text

    await update.message.reply_text(
        "کاربر گرامی لطفا آیدی تلگرامی خود را جهت ارتباط‌های بعدی وارد نمایید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_APP_FEE_TGID

# هندلر اپ فی - مرحله وارد کردن آیدی تلگرام
async def italy_app_fee_tgid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    مرحله وارد کردن آیدی تلگرام
    """
    text = update.message.text
    if text == "بازگشت":
        # بازگشت به مرحله قبلی (مقطع و رشته)
        await update.message.reply_text(
            "کاربر گرامی لطفا مقطع مورد نظر و رشته‌ی درخواستی را وارد کنید:",
            reply_markup=back_button_keyboard()
        )
        return States.ITALY_APP_FEE_DEGREE

    context.user_data["id"] = text

    await update.message.reply_text(
        "کاربر گرامی لطفا شماره تماس خود را جهت پیگیری‌های آتی وارد نمایید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_APP_FEE_CONTACT

# هندلر اپ فی - مرحله وارد کردن شماره تماس
async def italy_app_fee_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    مرحله وارد کردن شماره تماس
    """
    text = update.message.text
    if text == "بازگشت":
        # بازگشت به مرحله قبلی (آیدی تلگرام)
        await update.message.reply_text(
            "کاربر گرامی لطفا آیدی تلگرامی خود را جهت ارتباط‌های بعدی وارد نمایید:",
            reply_markup=back_button_keyboard()
        )
        return States.ITALY_APP_FEE_TGID

    context.user_data["contact"] = text

    await update.message.reply_text(
        "لطفا مبلغ دقیق اپلیکشن فی کورس درخواستی خود را به یورو وارد کنید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_APP_FEE_AMOUNT

# هندلر اپ فی - مرحله وارد کردن مبلغ به یورو و محاسبه ریالی
async def italy_app_fee_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    مرحله دریافت مبلغ اپ فی به یورو و محاسبه ریالی
    """
    text = update.message.text
    if text == "بازگشت":
        # بازگشت به مرحله قبلی (شماره تماس)
        await update.message.reply_text(
            "کاربر گرامی لطفا شماره تماس خود را جهت پیگیری‌های آتی وارد نمایید:",
            reply_markup=back_button_keyboard()
        )
        return States.ITALY_APP_FEE_CONTACT

    try:
        amount_eur = float(text)
        if amount_eur <= 0:
            raise ValueError

        context.user_data["app_fee_euro_amount"] = amount_eur
        euro_price, unit = await get_euro_to_toman_exchange_rate()
        context.user_data["app_fee_euro_price"] = euro_price
        # محاسبه ریالی با نرخ ثابت 87000
        amount_rial = int(amount_eur * euro_price * 10)
        context.user_data["app_fee_rial"] = amount_rial

        await update.message.reply_text(
            f"با توجه به اطلاعات وارده، هزینه‌ی درخواست جاری {amount_rial} ریال می‌باشد.\n"
            "جهت ادامه، یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=app_fee_confirm_keyboard()
        )
        return States.ITALY_APP_FEE_CONFIRM

    except ValueError:
        await update.message.reply_text(
            "لطفا یک مقدار معتبر به یورو وارد کنید.",
            reply_markup=back_button_keyboard()
        )
        return States.ITALY_APP_FEE_AMOUNT

# هندلر اپ فی - مرحله تأیید پرداخت یا انصراف
async def italy_app_fee_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    مرحله نمایش مبلغ ریالی و دریافت تصمیم کاربر (پرداخت / انصراف)
    """
    text = update.message.text
    if text == "بازگشت":
        # بازگشت به مرحله وارد کردن مبلغ
        amount_rial = context.user_data.get("app_fee_rial")
        await update.message.reply_text(
            f"هزینه‌ی درخواست جاری {amount_rial} ریال می‌باشد.\n"
            "اگر تمایل به پرداخت دارید روی 'پرداخت' بزنید، در غیر این صورت 'انصراف':",
            reply_markup=app_fee_confirm_keyboard()
        )
        return States.ITALY_APP_FEE_CONFIRM

    elif text == "پرداخت":
        amount_rial = context.user_data.get("app_fee_rial", 0)
        card_number = "9876-5432-1098-7654"  # شماره کارت دلخواه
        await update.message.reply_text(
            f"لطفا جهت پرداخت هزینه {amount_rial} ریال، مبلغ مذکور را به شماره کارت {card_number} واریز نمایید.\n"
            "سپس فیش پرداختی خود را در همین ربات ارسال کنید (عکس فیش را بفرستید).",
            reply_markup=back_button_keyboard()
        )
        return States.ITALY_APP_FEE_RECEIPT

    elif text == "انصراف":
        await update.message.reply_text(
            "عملیات اپ فی لغو شد. برای بازگشت به منوی اصلی، /start را بزنید یا از منو انتخاب کنید.",
            reply_markup=main_menu_keyboard()
        )
        return States.MAIN_MENU

    else:
        await update.message.reply_text(
            "گزینه نامعتبر. لطفا پرداخت یا انصراف را انتخاب کنید.",
            reply_markup=app_fee_confirm_keyboard()
        )
        return States.ITALY_APP_FEE_CONFIRM

# هندلر اپ فی - مرحله دریافت فیش پرداخت
async def italy_app_fee_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    مرحله دریافت فیش پرداخت برای اپ فی
    """
    if update.message.text == "بازگشت":
        # بازگشت به مرحله تایید پرداخت
        amount_rial = context.user_data.get("app_fee_rial", 0)
        await update.message.reply_text(
            f"هزینه‌ی درخواست جاری {amount_rial} ریال می‌باشد.\n"
            "اگر قصد پرداخت دارید، مبلغ را واریز و فیش را ارسال کنید یا انصراف:",
            reply_markup=app_fee_confirm_keyboard()
        )
        return States.ITALY_APP_FEE_CONFIRM

    if update.message.photo:
        save_directory = "saved_photo/app_and_tuition_fee"
        file_path = await save_transaction_photo(update, context, save_directory)
        context.user_data["app_fee_trans_filepath"] = file_path


        if context.user_data["is_app_fee"]:
            app_fee_control(update, context)
        else:
            tuition_fee_control(update, context)


        # در صورت دریافت عکس
        await update.message.reply_text(
            "کاربر گرامی، درخواست شما با موفقیت ثبت شد. "
            "ادمین‌های پرداختی ما در سریع‌ترین فرصت با شما ارتباط خواهند گرفت.",
            reply_markup=main_menu_keyboard()
        )

        return States.MAIN_MENU
    else:
        await update.message.reply_text(
            "لطفا یک عکس از فیش پرداختی خود ارسال کنید.",
            reply_markup=back_button_keyboard()
        )
        return States.ITALY_APP_FEE_RECEIPT



# هندلر تکمیل سفارشات قبلی - دریافت شماره سفارش
async def takmil_order_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        await update.message.reply_text(
            "Welcome! Choose an option:",
            reply_markup=main_menu_keyboard()
        )
        return States.MAIN_MENU
    # ذخیره شماره سفارش
    context.user_data["takmil_order_number"] = text
    await update.message.reply_text(
        "لطفا مبلغ قابل پرداخت برای سفارش خود را به ریال وارد نمایید:",
        reply_markup=back_button_keyboard()
    )
    return States.TAKMIL_AMOUNT

# هندلر تکمیل سفارشات قبلی - دریافت مبلغ
async def takmil_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        await update.message.reply_text(
            "لطفا شماره سفارشی را که از ادمین های پرداختی دریافت کرده اید را وارد کنید:",
            reply_markup=back_button_keyboard()
        )
        return States.TAKMIL_ORDER_NUMBER
    if text.isdigit():
        amount = text
        context.user_data["takmil_amount"] = amount
        card_number = "XXXX-XXXX-XXXX-1234"  # جایگزین با شماره کارت واقعی
        await update.message.reply_text(
            f"مبلغ قابل پرداخت {amount} ریال می‌باشد. اگر صحیح است، لطفاً رسید واریزی خود را به شماره کارت {card_number} در ربات ارسال نمایید.",
            reply_markup=back_button_keyboard()
        )
        return States.TAKMIL_RECEIPT
    else:
        await update.message.reply_text(
            "لطفا یک عدد معتبر وارد کنید.",
            reply_markup=back_button_keyboard()
        )
        return States.TAKMIL_AMOUNT

# هندلر تکمیل سفارشات قبلی - دریافت رسید واریزی
async def takmil_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        await update.message.reply_text(
            "لطفا مبلغ قابل پرداخت برای سفارش خود را به ریال وارد نمایید:",
            reply_markup=back_button_keyboard()
        )
        return States.TAKMIL_AMOUNT
    context.user_data["takmil_receipt"] = text
    # پردازش داده‌ها یا ارسال به ادمین
    await update.message.reply_text(
        "رسید واریزی شما دریافت شد. ادمین‌های ما در سریع‌ترین حالت با شما تماس خواهند گرفت.",
        reply_markup=main_menu_keyboard()
    )
    return States.MAIN_MENU

# هندلر لغو عملیات (اختیاری)
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "عملیات لغو شد. برای شروع مجدد /start را بزنید.",
        reply_markup=ReplyKeyboardMarkup(
            [["/start"]], resize_keyboard=True
        )
    )
    return ConversationHandler.END



def cimea_type_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton("comparability+verification")], [KeyboardButton("comparability")], [KeyboardButton("بازگشت")]],
        resize_keyboard=True,
    )

def cimea_speed_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton("فوری")], [KeyboardButton("عادی")], [KeyboardButton("بازگشت")]],
        resize_keyboard=True,
    )

def cimea_confirm_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton("پرداخت")], [KeyboardButton("انصراف")]],
        resize_keyboard=True,
    )

async def italy_cimea_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "کاربر گرامی لطفا از بین گزینه های زیر نوع درخواست خود را مشخص کنید." 
        "(اگر برای دیپلم ثبت درخواست گواهی چیمه آ دارید صرفا میتوانید ثبت درخواست comparability کنید)",
        reply_markup=cimea_type_keyboard()
    )
    return States.ITALY_CIMEA_TYPE

async def italy_cimea_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await italy_main_menu(update, context)
    context.user_data["cimea_type"] = text
    await update.message.reply_text(
        "کاربر گرامی لطفا از بین گزینه های زیر نوع درخواست خود را مشخص کنید."
        "(درخواست عادی در بازه زمانی دوماهه و درخواست فوری در بازه زمانی یک ماهه قابل بررسی است)",
        reply_markup=cimea_speed_keyboard()
    )
    return States.ITALY_CIMEA_SPEED

async def italy_cimea_speed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await italy_cimea_payment(update, context)
    context.user_data["cimea_speed"] = text
    
    price_map = {
        ("comparability+verification", "فوری"): 15000000,
        ("comparability+verification", "عادی"): 12000000,
        ("comparability", "فوری"): 10000000,
        ("comparability", "عادی"): 8000000,
    }
    price = price_map.get((context.user_data["cimea_type"], text), 0)
    context.user_data["cimea_price"] = price
    
    await update.message.reply_text(
        f"با توجه به اطلاعات وارده هزینه درخواست جاری {price} ریال می‌باشد. آیا مایل به ادامه ی درخواست خود هستید؟",
        reply_markup=cimea_confirm_keyboard()
    )
    return States.ITALY_CIMEA_CONFIRM

async def italy_cimea_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "انصراف":
        return await italy_main_menu(update, context)
    elif text == "پرداخت":
        price = context.user_data["cimea_price"]
        await update.message.reply_text(
            f"لطفا جهت پرداخت درخواست جاری به مبلغ {price} ریال و تکمیل سفارش خود هزینه مذکور را به شماره کارت 1234-5678-9012-3456 واریز نمایید و فیش پرداختی خود را در ربات ارسال نمایید."
        )
        return States.ITALY_CIMEA_RECEIPT_ID
    
# هندلر دریافت آیدی تلگرام بعد از تایید درخواست
async def italy_cimea_receive_tg_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await italy_cimea_speed(update, context)

    # ذخیره آیدی تلگرام
    context.user_data["id"] = text

    # درخواست شماره تماس از کاربر
    await update.message.reply_text(
        "لطفا شماره تماس خود را وارد کنید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_CIMEA_RECEIPT_PHONE

# هندلر دریافت شماره تماس بعد از آیدی تلگرام
async def italy_cimea_receive_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await italy_cimea_receive_tg_id(update, context)

    # ذخیره شماره تماس
    context.user_data["contact"] = text

    # تایید نهایی و ارسال فیش پرداخت
    price = context.user_data.get("cimea_price", 0)
    await update.message.reply_text(
        f"لطفا جهت پرداخت درخواست جاری به مبلغ {price} ریال، هزینه مذکور را به شماره کارت 1234-5678-9012-3456 واریز نمایید و فیش پرداختی خود را در ربات ارسال نمایید.",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_CIMEA_RECEIPT


async def italy_cimea_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.photo:
        await update.message.reply_text(
            "کاربر گرامی درخواست شما با موفقیت ثبت شد. ادمین‌های پرداختی ما در سریع‌ترین فرصت با شما ارتباط خواهند گرفت.",
            reply_markup=main_menu_keyboard()
        )
        return States.MAIN_MENU
    else:
        await update.message.reply_text("لطفا یک تصویر از فیش پرداختی خود ارسال کنید.")
        return States.ITALY_CIMEA_RECEIPT


# هندلر ثبت نام دانشگاه در Italy
async def italy_register_university(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        return await italy_main_menu(update, context)

    # درخواست نام دانشگاه از کاربر
    await update.message.reply_text(
        "لطفا نام دانشگاه مدنظر که میخواهید پروسه Enrollment/apply را برای آن آغاز کنید وارد نمایید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_REGISTER_UNIVERSITY_NAME

# هندلر دریافت نام دانشگاه
async def italy_register_university_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        return await italy_register_university(update, context)
    
    context.user_data["university_name"] = update.message.text

    # نمایش گزینه‌های نوع درخواست
    await update.message.reply_text(
        "لطفا نوع درخواست خود را مشخص کنید:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_reg_type(),
            resize_keyboard=True,
        )
    )
    return States.ITALY_REGISTER_UNIVERSITY_TYPE

# هندلر انتخاب نوع درخواست
async def italy_register_university_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        await update.message.reply_text(
            "لطفا نام دانشگاه مدنظر که میخواهید پروسه Enrollment/apply را برای آن آغاز کنید وارد نمایید:",
            reply_markup=back_button_keyboard()
        )
        return States.ITALY_REGISTER_UNIVERSITY_NAME

    context.user_data["university_type"] = get_id_by_regTypeName_control(update.message.text)
    # درخواست نام کورس
    await update.message.reply_text(
        "لطفا نام کورس را انتخاب کنید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_REGISTER_UNIVERSITY_COURSE

# هندلر انتخاب نام کورس
async def italy_register_university_course(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        await update.message.reply_text(
            "لطفا نوع درخواست خود را مشخص کنید:",
            reply_markup=reply_keyboard_reg_type()
        )
        return States.ITALY_REGISTER_UNIVERSITY_TYPE
    context.user_data["course_name"] = update.message.text
    # درخواست مقطع کورس
    await update.message.reply_text(
        "لطفا مقطع کورس خود را انتخاب کنید:",
        reply_markup=reply_keyboard_reg_course_level()
    )
    return States.ITALY_REGISTER_UNIVERSITY_DEGREE

# هندلر انتخاب مقطع کورس
async def italy_register_university_degree(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        await update.message.reply_text(
            "لطفا نام کورس را انتخاب کنید:",
            reply_markup=back_button_keyboard()
        )
        return States.ITALY_REGISTER_UNIVERSITY_COURSE
    context.user_data["course_level"] = get_id_by_regCourseLevelName_control(update.message.text)
    # درخواست زبان کورس
    await update.message.reply_text(
        "لطفا زبان کورس خود را انتخاب کنید:",
        reply_markup=reply_keyboard_reg_course_lang()
    )
    return States.ITALY_REGISTER_UNIVERSITY_LANGUAGE

# هندلر انتخاب زبان کورس
async def italy_register_university_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        await update.message.reply_text(
            "لطفا مقطع کورس خود را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard_reg_course_level(),
                resize_keyboard=True,
            )
        )
        return States.ITALY_REGISTER_UNIVERSITY_DEGREE
    context.user_data["course_lang"] = get_id_by_regCourseLangName_control(update.message.text)
    # درخواست آیدی تلگرام از کاربر
    await update.message.reply_text(
        "لطفا آیدی تلگرامی خود را وارد نمایید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_REGISTER_UNIVERSITY_TGID

# هندلر دریافت آیدی تلگرام
async def italy_register_university_tgid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        await update.message.reply_text(
            "لطفا زبان کورس خود را انتخاب کنید:",
            reply_markup=reply_keyboard_reg_course_lang()
        )
        return States.ITALY_REGISTER_UNIVERSITY_LANGUAGE
    context.user_data["id"] = update.message.text
    # درخواست شماره تماس از کاربر
    await update.message.reply_text(
        "لطفا شماره تماس خود را وارد کنید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_REGISTER_UNIVERSITY_CONTACT

# هندلر دریافت شماره تماس
async def italy_register_university_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        await update.message.reply_text(
            "لطفا آیدی تلگرامی خود را وارد نمایید:",
            reply_markup=back_button_keyboard()
        )
        return States.ITALY_REGISTER_UNIVERSITY_TGID

    context.user_data["contact"] = update.message.text

    reg_uni_control(update, context)

    # نمایش پیام نهایی و بازگشت به منوی اصلی
    await update.message.reply_text(
        "ادمین های پرداختی جهت دریافت اطلاعات بیشتر از شما در راستای تکمیل سفارش ارتباط خواهند گرفت.",
        reply_markup=main_menu_keyboard()
    )
    return States.MAIN_MENU




# هندلر رزرو هتل و هواپیما در Italy
async def italy_reserve_hotel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # چک کردن بازگشت
    if update.message.text == "بازگشت":
        await update.message.reply_text(
            "لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=italy_main_menu_keyboard()
        )
        return States.ITALY_MAIN_MENU
    
    # درخواست آیدی تلگرام از کاربر
    await update.message.reply_text(
        "کاربر گرامی لطفا آیدی تلگرامی خود را جهت ارتباط ادمین های پرداختی وارد نمایید:",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("بازگشت")]
            ],
            resize_keyboard=True,
        )
    )
    return States.ITALY_RESERVE_HOTEL_TGID

# هندلر آیدی تلگرام برای رزرو هتل و هواپیما
async def italy_reserve_hotel_tgid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        return await italy_reserve_hotel(update, context)

    context.user_data["id"] = update.message.text
    # درخواست شماره تماس از کاربر
    await update.message.reply_text(
        "کاربر گرامی لطفا شماره تماس خود را جهت پیگیری های آتی برای سفارش خود وارد کنید:",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("بازگشت")]
            ],
            resize_keyboard=True,
        )
    )
    return States.ITALY_RESERVE_HOTEL_CONTACT

# هندلر شماره تماس برای رزرو هتل و هواپیما
async def italy_reserve_hotel_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        return await italy_reserve_hotel_tgid(update, context)

    context.user_data["contact"] = update.message.text
    # نمایش پیام نهایی و بازگشت به منوی اصلی
    await update.message.reply_text(
        "ادمین های پرداختی جهت دریافت اطلاعات بیشتر از شما در راستای تکمیل سفارش ارتباط خواهند گرفت.",
        reply_markup=main_menu_keyboard()
    )
    return States.MAIN_MENU
