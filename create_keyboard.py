from model import (get_reg_type, get_reg_course_level, get_reg_course_lang, get_tolc_exam_type,
                   get_tolcExamDetailName_by_tolcExamTypeId, get_cimea_type, get_cimea_speed)
from telegram import KeyboardButton, ReplyKeyboardMarkup
max_col = 2


def dynamic_create_keyboard(result):
    btns = []
    temp_group = []
    key = list(result[0].keys())[-1]

    for i, item in enumerate(result):
        temp_group.append(KeyboardButton(item[key]))
        # Add the current group to btns when it has max_col items, or if it's the last item
        if len(temp_group) == max_col or i == len(result) - 1:
            btns.append(temp_group)
            temp_group = []
    
    btns.append([KeyboardButton("بازگشت")])
    return ReplyKeyboardMarkup(
        btns,
        resize_keyboard=True,
    )



def reply_keyboard_reg_type():
    result = get_reg_type()
    return dynamic_create_keyboard(result)
    

def reply_keyboard_reg_course_level():
    result = get_reg_course_level()
    return dynamic_create_keyboard(result)


def reply_keyboard_reg_course_lang():
    result = get_reg_course_lang()
    return dynamic_create_keyboard(result)


def reply_keyboard_tolc_exam_type():
    result = get_tolc_exam_type()
    return dynamic_create_keyboard(result)


def reply_keyboard_tolc_exam_detail(tolcExamTypeId):
    result = get_tolcExamDetailName_by_tolcExamTypeId(tolcExamTypeId)
    return dynamic_create_keyboard(result)


def reply_keyboard_cimea_type():
    result = get_cimea_type()
    return dynamic_create_keyboard(result)


def reply_keyboard_cimea_speed():
    result = get_cimea_speed()
    return dynamic_create_keyboard(result)






def back_button_keyboard() -> ReplyKeyboardMarkup:
    back_btn = KeyboardButton("بازگشت")
    return ReplyKeyboardMarkup(
        [
            [back_btn],
        ],
        resize_keyboard=True,
    )


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    italy_btn = KeyboardButton("\U0001F1EE\U0001F1F9 Italy")
    buy_euro_btn = KeyboardButton("خرید یورو \U0001F4B2")

    others_btn = KeyboardButton("others")
    return ReplyKeyboardMarkup(
        [
            [italy_btn],
            [buy_euro_btn, others_btn],
        ],
        resize_keyboard=True,
    )


def admin_menu_keyboard() -> ReplyKeyboardMarkup:
    broadcast_btn = KeyboardButton("پیام همگانی")
    finish_btn = KeyboardButton("سفارش‌های تکمیل نشده")
    unfinish_btn = KeyboardButton("سفارش‌های تکمیل شده")
    return ReplyKeyboardMarkup(
        [
            [broadcast_btn],
            [finish_btn, unfinish_btn],
        ],
        resize_keyboard=True,
    )


def isfinish_order_keyboard(isfinish_text) -> ReplyKeyboardMarkup:
    next_btn = KeyboardButton("بعدی")
    prev_btn = KeyboardButton("قبلی")
    isfinish_btn = KeyboardButton(isfinish_text)
    back_btn = KeyboardButton("بازگشت")
    return ReplyKeyboardMarkup(
        [
            [next_btn, prev_btn],
            [isfinish_btn],
            [back_btn],
        ],
        resize_keyboard=True,
    )




def italy_main_menu_keyboard() -> ReplyKeyboardMarkup:
    reserve_exam_btn = KeyboardButton("رزرو آزمون")
    cimea_payment_btn = KeyboardButton("پرداخت چیمه آ(CIMEA)")
    app_fee_btn = KeyboardButton("اپ فی")
    uni_tui_btn = KeyboardButton("شهریه دانشگاه")
    register_university_btn = KeyboardButton("ثبت نام دانشگاه")
    reserve_hotel_btn = KeyboardButton("رزرو هتل و هواپیما")
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


def pay_cancel_keyboard() -> ReplyKeyboardMarkup:
    pay_btn = KeyboardButton("پرداخت")
    cancel_btn = KeyboardButton("انصراف")
    back_btn = KeyboardButton("بازگشت")
    return ReplyKeyboardMarkup(
        [
            [pay_btn, cancel_btn],
            [back_btn],
        ],
        resize_keyboard=True,
    )


def yes_no_keyboard():
    yes_btn = KeyboardButton("بله")
    no_btn = KeyboardButton("خیر")
    back_btn = KeyboardButton("بازگشت")
    return ReplyKeyboardMarkup(
        [
            [yes_btn, no_btn],
            [back_btn]
        ],
        resize_keyboard=True,
    )

