from model import get_reg_type, get_reg_course_level
from telegram import KeyboardButton
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
    return btns


def btn_reg_type():
    result = get_reg_type()
    return create_btns(result)
    

def btn_reg_course_level():
    result = get_reg_course_level()
    return create_btns(result)