from model import (get_user_by_id, insert_user, update_user, insert_buy_currency, insert_other_order,
                   insert_app_fee, insert_tuition_fee, get_id_by_regTypeName, get_id_by_regCourseLevelName, get_id_by_regCourseLangName,
                   insert_reg_uni, get_id_by_tolcExamTypeName, get_id_by_tolcExamDetailName, insert_cisia_account, insert_tolc_order_exam,
                   get_cisia_account_by_tel_userId, update_cisia_account, insert_torvergata, get_id_by_cimeaTypeName,
                   get_id_by_cimeaSpeedName, get_cimeaPrice_by_cimeaTypeAndSpeedId, get_telUserId, insert_cimea, insert_reserve_hotel,
                   get_admin_by_tel_userId,get_buyEuro_admin,
                   get_otherOrder_admin,get_reserveHotel_admin, get_regUni_admin, get_tuitionFee_admin, get_cimea_admin,get_appFee_admin,
                   get_toevergata_admin, get_tolcExam_admin, update_finish)

from encrypt.password_encryption import encrypting_password,decrypting_password


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

def get_telUserId_control():
    list_user = []
    x = get_telUserId()
    for xx in x:
        list_user.append(xx['tel_userId'])
    return list_user


async def broadcast_message(context, message):
    users = get_telUserId()
    for user_id in users:
        try:
            await context.application.bot.send_message(chat_id=user_id["tel_userId"], text=message)
        except Exception as e:
            print(f"{user_id},{e}")




def insert_or_update_user(update, context):
    user = get_user_by_id(context._user_id)
    if not context.user_data.get("contact") and len(user) !=0: # multiple start but no order
        context.user_data["contact"] = user[0].get("phoneNumber", "No phone number found")
        context.user_data["id"] = user[0]["userName"]
    if len(user) == 0:
        insert_user(userId=context._user_id, userName=context.user_data.get("id", update.message.from_user.username),
                    userFirstName=update.message.from_user.first_name, userLastName=update.message.from_user.last_name,
                    phoneNumber=context.user_data.get("contact", " "))
    else:
        update_user(userId=context._user_id, userName=context.user_data.get("id", update.message.from_user.username),
                    userFirstName=update.message.from_user.first_name, userLastName=update.message.from_user.last_name,
                    phoneNumber=context.user_data.get("contact", " "))
        


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
    insert_buy_currency(tel_userId=context._user_id, currencyId=1, value=context.user_data["amount"], finish=0)


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

def reserve_hotel_control(update, context):
    insert_or_update_user(update, context)
    insert_reserve_hotel(context._user_id, finish=0)

def get_admin_control(update, context):
    result = get_admin_by_tel_userId(context._user_id)
    return len(result)


def print_order_buyEuro(finish):
    data = get_buyEuro_admin(finish)

    formatted_list = [
    (
        f"🆔شناسه خرید:\n{item['buyCurrencyId']}\n\n"
        f"⏰زمان:\n{item['time'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"👤نام:\n{item['userFirstName']} {item['userLastName'] if item['userLastName'] else 'نامشخص'}\n\n"
        f"🏷نام کاربری:\n{item['userName']}\n\n"
        f"📞تلفن:\n{item['phoneNumber']}\n\n"
        f"💰مقدار:\n{item['value']}\n\n"
        f"💱ارز:\n{item['currency_name']}\n\n"
        f"📌نوع پرداختی:\nخرید یورو\n\n"
        f"{'-'*50}\n"
        f"result10",
        None  # Second element of the tuple
    )
    for item in data
    ]

    return formatted_list


def print_order_otherOrder(finish):
    data = get_otherOrder_admin(finish)

    formatted_list = [(
        f"🆔شناسه سفارش:\n{item['orderOtherId']}\n\n"
        f"⏰زمان:\n{item['time'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"👤نام:\n{item['userFirstName']} {item['userLastName'] if item['userLastName'] else 'نامشخص'}\n\n"
        f"🏷نام کاربری:\n{item['userName']}\n\n"
        f"📞تلفن:\n{item['phoneNumber']}\n\n"
        f"📝توضیحات:\n{item['description']}\n\n"
        f"💰قیمت:\n{item['price']}\n\n"
        f"📌نوع پرداختی:\nothers\n\n"
        f"{'-'*50}\n"
        f"result11",
        None)
        for item in data
    ]

    return formatted_list


def print_order_reserveHotel(finish):
    data = get_reserveHotel_admin(finish)

    formatted_list = [(
        f"🆔شناسه رزرو:\n{item['reserveHotelID']}\n\n"
        f"⏰زمان:\n{item['time'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"👤نام:\n{item['userFirstName']} {item['userLastName'] if item['userLastName'] else 'نامشخص'}\n\n"
        f"🏷نام کاربری:\n{item['userName']}\n\n"
        f"📞تلفن:\n{item['phoneNumber']}\n\n"
        f"🏨نوع پرداختی:\nرزرو هتل\n\n"
        f"{'-'*50}\n"
        f"result12",
        None)
        for item in data
    ]
    return formatted_list


def print_order_reguni(finish):
    data = get_regUni_admin(finish)

    formatted_list = [(
        f"🆔شناسه ثبت‌نام:\n{item['regUniId']}\n\n"
        f"⏰زمان:\n{item['time'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"👤نام:\n{item['userFirstName']} {item['userLastName'] if item['userLastName'] else 'نامشخص'}\n\n"
        f"🏷نام کاربری:\n{item['userName']}\n\n"
        f"📞تلفن:\n{item['phoneNumber']}\n\n"
        f"📚نوع ثبت‌نام:\n{item['regTypeName']}\n\n"
        f"🎓مقطع تحصیلی:\n{item['regCourseLevelName']}\n\n"
        f"🗣زبان دوره:\n{item['regCourseLangName']}\n\n"
        f"🏛دانشگاه:\n{item['uniName']}\n\n"
        f"📖نام رشته/دوره:\n{item['courseName']}\n\n"
        f"📌نوع پرداختی:\nثبت‌نام دانشگاه\n\n"
        f"{'-'*50}\n"
        f"result13",None)
        for item in data
    ]

    return formatted_list


def print_order_tuitionFee(finish):
    data = get_tuitionFee_admin(finish)
    formatted_list = [
        (
            f"🆔شناسه پرداخت شهریه:\n{item['tuitionFeeId']}\n\n"
            f"⏰زمان:\n{item['time'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"👤نام:\n{item['userFirstName']} {item['userLastName'] if item['userLastName'] else 'نامشخص'}\n\n"
            f"🏷نام کاربری:\n{item['userName']}\n\n"
            f"📞تلفن:\n{item['phoneNumber']}\n\n"
            f"🏛دانشگاه:\n{item['university']}\n\n"
            f"🎓مدرک تحصیلی:\n{item['degree']}\n\n"
            f"💶مقدار یورو:\n{item['euroAmount']}\n\n"
            f"💱قیمت یورو:\n{item['euroPrice']}\n\n"
            f"💰مبلغ نهایی (ریال):\n{item['rial_change']}\n\n"
            f"📌نوع پرداختی:\nپرداخت شهریه\n\n"
            f"{'-'*50}\n"
            f"result14",
            item['trans_filepath']  # Transaction file in the second field of tuple
        )
        for item in data
    ]

    return formatted_list


def print_order_cimea(finish):
    data = get_cimea_admin(finish)

    formatted_list = [
    (
        f"🆔شناسه CIMEA:\n{item['cimeaId']}\n\n"
        f"⏰زمان:\n{item['time'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"👤نام:\n{item['userFirstName']} {item['userLastName'] if item['userLastName'] else 'نامشخص'}\n\n"
        f"🏷نام کاربری:\n{item['userName']}\n\n"
        f"📞تلفن:\n{item['phoneNumber']}\n\n"
        f"💰قیمت:\n{item['cimeaPrice']} \n\n"
        f"🚀سرعت بررسی:\n{item['cimeaSpeedName']}\n\n"
        f"📄نوع مقایسه:\n{item['cimeaTypeName']}\n\n"
        f"📌نوع پرداختی:\nCIMEA\n\n"
        f"{'-'*50}\n"
        f"result15",
        item['trans_filepath']  # Transaction file in second field of tuple
        )
        for item in data
    ]

    return formatted_list


def print_order_appFee(finish):
    data = get_appFee_admin(finish)

    formatted_list = [
    (
        f"🆔شناسه پرداخت اپلیکیشن فی:\n{item['appFeeId']}\n\n"
        f"⏰زمان:\n{item['time'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"👤نام:\n{item['userFirstName']} {item['userLastName'] if item['userLastName'] else 'نامشخص'}\n\n"
        f"🏷نام کاربری:\n{item['userName']}\n\n"
        f"📞تلفن:\n{item['phoneNumber']}\n\n"
        f"🏛دانشگاه:\n{item['university']}\n\n"
        f"🎓مدرک تحصیلی:\n{item['degree']}\n\n"
        f"💶مقدار یورو:\n{item['euroAmount']}\n\n"
        f"💱قیمت یورو:\n{item['euroPrice']}\n\n"
        f"💰مبلغ نهایی (ریال):\n{item['rialchange']}\n\n"
        f"📌نوع پرداختی:\nپرداخت اپلیکیشن فی\n\n"
        f"{'-'*50}\n"
        f"result16",
        item['trans_filepath']  # Transaction file in second field of tuple
        )
        for item in data
    ]

    return formatted_list


def print_order_tovergata(finish):
    data = get_toevergata_admin(finish)

    formatted_list = [
        (
            f"🆔شناسه پرداخت Tor Vergata:\n{item['torvergataId']}\n\n"
            f"⏰زمان:\n{item['time'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"👤نام:\n{item['userFirstName']} {item['userLastName'] if item['userLastName'] else 'نامشخص'}\n\n"
            f"🏷نام کاربری:\n{item['userName']}\n\n"
            f"📞تلفن:\n{item['phoneNumber']}\n\n"
            f"📌نوع پرداختی:\nپرداخت Tor Vergata\n\n"
            f"{'-'*50}\n"
            f"result17",
            item['trans_filepath']  # Transaction file in second field of tuple
        )
        for item in data
    ]

    return formatted_list


def print_order_tolcExam(finish):
    data = get_tolcExam_admin(finish)

    formatted_list = [
    (
        f"🆔شناسه سفارش آزمون TOLC:\n{item['tolcOrderExamId']}\n\n"
        f"⏰زمان:\n{item['time'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"👤نام:\n{item['userFirstName']} {item['userLastName'] if item['userLastName'] else 'نامشخص'}\n\n"
        f"🏷نام کاربری:\n{item['userName']}\n\n"
        f"📞تلفن:\n{item['phoneNumber']}\n\n"
        f"📝نام آزمون:\n{item['tolcExamDetailName']}\n\n"
        f"📚نوع آزمون:\n{item['tolcExamTypeName']}\n\n"
        f"🔑نام کاربری چیزآ:\n{item['username']}\n\n"
        f"🔒رمز عبور چیزآ:\n{decrypting_password(item['password'])}\n\n"
        f"📌نوع پرداختی:\nسفارش آزمون TOLC\n\n"
        f"{'-'*50}\n"
        f"result18",
        item['trans_filePath']  # Transaction file in the second field of tuple
    )
    for item in data
    ]

    return formatted_list



def print_order(finish):
    data=[]
    for i in print_order_buyEuro(finish):
        data.append(i)
    for i in print_order_otherOrder(finish):
        data.append(i)
    for i in print_order_reserveHotel(finish):
        data.append(i)
    for i in print_order_reguni(finish):
        data.append(i)
    for i in print_order_tuitionFee(finish):
        data.append(i)
    for i in print_order_cimea(finish):
        data.append(i)
    for i in print_order_appFee(finish):
        data.append(i)
    for i in print_order_tovergata(finish):
        data.append(i)
    for i in print_order_tolcExam(finish):
        data.append(i)

    return data


def update_finish_controller(message,finish):
    id = int(message.split("\n")[1])
    print(id)
    table_id = int(message[-2:])
    print(table_id)
    if table_id == 10 :
        update_finish("buy_currency",finish,"buyCurrencyId",id)
    elif table_id == 11:
        update_finish("order_other",finish,"orderOtherId",id)
    elif table_id == 12:
        update_finish("reserve_hotel",finish,"reserveHotelID",id)
    elif table_id == 13:
        update_finish("reg_uni",finish,"regUniId",id)
    elif table_id == 14:
        update_finish("tuition_fee",finish,"tuitionFeeId",id)
    elif table_id == 15:
        update_finish("cimea",finish,"cimeaId",id)
    elif table_id == 16:
        update_finish("app_fee",finish,"appFeeId",id)
    elif table_id == 17:
        update_finish("torvergata",finish,"torvergataId",id)
    elif table_id == 18:
        update_finish("tolc_order_exam",finish,"tolcOrderExamId",id)