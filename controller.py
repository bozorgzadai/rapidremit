from model import (get_user_by_id, insert_user, update_user, insert_buy_currency, insert_other_order,
                   insert_app_fee, insert_tuition_fee, get_id_by_regTypeName, get_id_by_regCourseLevelName, get_id_by_regCourseLangName,
                   insert_reg_uni, get_id_by_tolcExamTypeName)


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

    





