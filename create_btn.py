from model import (get_reg_type, get_reg_course_level, get_reg_course_lang, get_tolc_exam_type,
                   get_tolcExamDetailName_by_tolcExamTypeId, get_cimea_type, get_cimea_speed)
from telegram import KeyboardButton, ReplyKeyboardMarkup
max_col = 2

def create_btns(result):
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
    return create_btns(result)
    

def reply_keyboard_reg_course_level():
    result = get_reg_course_level()
    return create_btns(result)


def reply_keyboard_reg_course_lang():
    result = get_reg_course_lang()
    return create_btns(result)


def reply_keyboard_tolc_exam_type():
    result = get_tolc_exam_type()
    return create_btns(result)


def reply_keyboard_tolc_exam_detail(tolcExamTypeId):
    result = get_tolcExamDetailName_by_tolcExamTypeId(tolcExamTypeId)
    return create_btns(result)


def reply_keyboard_cimea_type():
    result = get_cimea_type()
    return create_btns(result)


def reply_keyboard_cimea_speed():
    result = get_cimea_speed()
    return create_btns(result)