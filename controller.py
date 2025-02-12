from model import (get_user_by_id, insert_user, update_user, insert_buy_currency, insert_other_order,
                   insert_app_fee, insert_tuition_fee, get_id_by_regTypeName, get_id_by_regCourseLevelName, get_id_by_regCourseLangName,
                   insert_reg_uni, get_id_by_tolcExamTypeName, get_id_by_tolcExamDetailName, insert_cisia_account, insert_tolc_order_exam,
                   get_cisia_account_by_tel_userId, update_cisia_account, insert_torvergata, get_id_by_cimeaTypeName,
                   get_id_by_cimeaSpeedName, get_cimeaPrice_by_cimeaTypeAndSpeedId, insert_cimea)

from encrypt.password_encryption import encrypting_password


def get_id_by_regTypeName_control(regTypeName):
    result = get_id_by_regTypeName(regTypeName)
    key = list(result[0].keys())[0]
    return result[0][key]

def get_id_by_regCourseLevelName_control(regCourseLevelName):
    result = get_id_by_regCourseLevelName(regCourseLevelName)
    key = list(result[0].keys())[0]
    return result[0][key]

def get_id_by_regCourseLangName_control(regCourseLangName):
    result = get_id_by_regCourseLangName(regCourseLangName)
    key = list(result[0].keys())[0]
    return result[0][key]

def get_id_by_tolcExamTypeName_control(tolcExamTypeName):
    result = get_id_by_tolcExamTypeName(tolcExamTypeName)
    key = list(result[0].keys())[0]
    return result[0][key]

def get_id_by_tolcExamDetailName_control(tolcExamDetailName):
    result = get_id_by_tolcExamDetailName(tolcExamDetailName)
    key = list(result[0].keys())[0]
    return result[0][key]

def get_id_by_cimeaTypeName_control(cimeaTypeName):
    result = get_id_by_cimeaTypeName(cimeaTypeName)
    key = list(result[0].keys())[0]
    return result[0][key]

def get_id_by_cimeaSpeedName_control(cimeaSpeedName):
    result = get_id_by_cimeaSpeedName(cimeaSpeedName)
    key = list(result[0].keys())[0]
    return result[0][key]

def get_cimeaPrice_by_cimeaTypeAndSpeedId_control(cimeaTypeId, cimeaSpeedId):
    result = get_cimeaPrice_by_cimeaTypeAndSpeedId(cimeaTypeId, cimeaSpeedId)
    keys = list(result[0].keys())
    return result[0][keys[0]], result[0][keys[-1]]

    

def insert_or_update_user(update, context):
    user = get_user_by_id(context._user_id)
    if len(user) == 0:
        insert_user(userId=context._user_id, userName=context.user_data["id"],
                    userFirstName=update.message.from_user.first_name, userLastName=update.message.from_user.last_name,
                    phoneNumber=context.user_data["contact"])
    else:
        update_user(userId=context._user_id, userName=update.message.from_user.username,
                    userFirstName=update.message.from_user.first_name, userLastName=update.message.from_user.last_name,
                    phoneNumber=context.user_data["contact"])
        

def insert_or_update_cisia_account(context):
    encrypt_password = encrypting_password(context.user_data["cisia_account_password"])

    cisia_account = get_cisia_account_by_tel_userId(context._user_id)
    if len(cisia_account) == 0:
        insert_cisia_account(context._user_id, username=context.user_data["cisia_account_username"],
                         password=encrypt_password)
    else:
        update_cisia_account(context._user_id, username=context.user_data["cisia_account_username"],
                             password=encrypt_password)
        



def buy_euro_control(update, context):
    insert_or_update_user(update, context)
    insert_buy_currency(tel_userId=context._user_id, currencyId=1, value=context.user_data["amount"])


def other_order_control(update, context):
    insert_or_update_user(update, context)
    insert_other_order(context._user_id, description=context.user_data["description"],
                       price=context.user_data["amount"], finish=0)
    
def app_fee_control(update, context):
    insert_or_update_user(update, context)
    insert_app_fee(context._user_id, university=context.user_data["app_fee_university"], degree=context.user_data["app_fee_degree"],
                   euroAmount=context.user_data["app_fee_euro_amount"], euroPrice=context.user_data["app_fee_euro_price"],
                   rialChange=context.user_data["app_fee_rial"], trans_filepath=context.user_data["app_fee_trans_filepath"], finish=0)
    
def tuition_fee_control(update, context):
    insert_or_update_user(update, context)
    insert_tuition_fee(context._user_id, university=context.user_data["app_fee_university"], degree=context.user_data["app_fee_degree"],
                   euroAmount=context.user_data["app_fee_euro_amount"], euroPrice=context.user_data["app_fee_euro_price"],
                   rialChange=context.user_data["app_fee_rial"], trans_filepath=context.user_data["app_fee_trans_filepath"], finish=0)
    
def reg_uni_control(update, context):
    insert_or_update_user(update, context)
    insert_reg_uni(context._user_id, regTypeId=context.user_data["university_type"], regCourseLevelId=context.user_data["course_level"],
                   regCourseLangId=context.user_data["course_lang"], uniName=context.user_data["university_name"],
                   courseName=context.user_data["course_name"], finish=0)
    
def tolc_order_exam_control(update, context):
    insert_or_update_user(update, context)
    insert_tolc_order_exam(context._user_id, tolcExamDetailId=context.user_data["tolcExamDetailId"],
                           examDate=context.user_data["told_exam_date"], trans_filePath=context.user_data["tolc_exam_trans_filepath"],
                           finish=0)
    
def torvergata_control(update, context):
    insert_or_update_user(update, context)
    insert_torvergata(context._user_id, trans_filepath=context.user_data["torvergata_trans_filepath"], finish=0)

def cimea_control(update, context):
    insert_or_update_user(update, context)
    insert_cimea(context._user_id, cimeaPriceId=context.user_data["cimea_price_id"],
                 trans_filepath=context.user_data["cimea_trans_filepath"], finish=0)




