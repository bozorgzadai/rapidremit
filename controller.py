from model import (get_user_by_id, insert_user, update_user, insert_buy_currency, insert_other_order,
                   insert_app_fee, insert_tuition_fee, get_id_by_regTypeName, get_id_by_regCourseLevelName, get_id_by_regCourseLangName,
                   insert_reg_uni, get_id_by_tolcExamTypeName, get_id_by_tolcExamDetailName, insert_cisia_account, insert_tolc_order_exam,
                   get_cisia_account_by_tel_userId, update_cisia_account, insert_torvergata, get_id_by_cimeaTypeName,
                   get_id_by_cimeaSpeedName, get_cimeaPrice_by_cimeaTypeAndSpeedId, get_telUserId, insert_cimea, insert_reserve_hotel,
                   get_admin_by_tel_userId,get_buyEuro_admin,
                   get_otherOrder_admin,get_reserveHotel_admin, get_regUni_admin, get_tuitionFee_admin, get_cimea_admin,get_appFee_admin,
                   get_toevergata_admin, get_tolcExam_admin, update_finish, get_orders_type_by_type, insert_orders,
                   get_orders_desc_by_ordersTypeId)

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

def get_id_by_ordersType_control(ordersType):
    result = get_orders_type_by_type(ordersType)
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

def insert_and_get_ordersId(ordersType):
    ordersTypeId = get_id_by_ordersType_control(ordersType)
    insert_orders(ordersTypeId)
    result = get_orders_desc_by_ordersTypeId(ordersTypeId)
    key = list(result[0].keys())[0]
    return result[0][key]




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
    ordersId = insert_and_get_ordersId("buy_currency")
    insert_buy_currency(tel_userId=context._user_id, ordersId=ordersId, currencyId=1, value=context.user_data["amount"], finish=0)


def other_order_control(update, context):
    insert_or_update_user(update, context)
    ordersId = insert_and_get_ordersId("order_other")
    insert_other_order(context._user_id, ordersId=ordersId, description=context.user_data["description"],
                       price=context.user_data["amount"], finish=0)
    
def app_fee_control(update, context):
    insert_or_update_user(update, context)
    ordersId = insert_and_get_ordersId("app_fee")
    insert_app_fee(context._user_id, ordersId=ordersId, university=context.user_data["app_fee_university"], degree=context.user_data["app_fee_degree"],
                   euroAmount=context.user_data["app_fee_euro_amount"], euroPrice=context.user_data["app_fee_euro_price"],
                   rialChange=context.user_data["app_fee_rial"], trans_filepath=context.user_data["app_fee_trans_filepath"], finish=0)
    
def tuition_fee_control(update, context):
    insert_or_update_user(update, context)
    ordersId = insert_and_get_ordersId("tuition_fee")
    insert_tuition_fee(context._user_id, ordersId=ordersId, university=context.user_data["app_fee_university"], degree=context.user_data["app_fee_degree"],
                        finish=0)
    
def reg_uni_control(update, context):
    insert_or_update_user(update, context)
    ordersId = insert_and_get_ordersId("reg_uni")
    insert_reg_uni(context._user_id, ordersId=ordersId, regTypeId=context.user_data["university_type"], regCourseLevelId=context.user_data["course_level"],
                   regCourseLangId=context.user_data["course_lang"], uniName=context.user_data["university_name"],
                   courseName=context.user_data["course_name"], finish=0)
    
def tolc_order_exam_control(update, context):
    insert_or_update_user(update, context)
    ordersId = insert_and_get_ordersId("tolc_order_exam")
    insert_tolc_order_exam(context._user_id, ordersId=ordersId, tolcExamDetailId=context.user_data["tolcExamDetailId"],
                           euroAmount=context.user_data["tolc_euro_amount"],
                           euroPrice=context.user_data["tolc_euro_price"],
                           rial_change=context.user_data["tolc_rial"],
                           examDate=context.user_data["told_exam_date"], trans_filePath=context.user_data["tolc_exam_trans_filepath"],
                           finish=0)
    
def torvergata_control(update, context):
    insert_or_update_user(update, context)
    ordersId = insert_and_get_ordersId("torvergata")
    insert_torvergata(context._user_id, ordersId=ordersId, euroAmount=context.user_data["torvergata_euro_amount"],
                      euroPrice=context.user_data["torvergata_euro_price"],
                      rial=context.user_data["torvergata_rial"],
                      trans_filepath=context.user_data["torvergata_trans_filepath"], finish=0)

def cimea_control(update, context):
    insert_or_update_user(update, context)
    ordersId = insert_and_get_ordersId("cimea")
    insert_cimea(context._user_id, ordersId=ordersId, cimeaPriceId=context.user_data["cimea_price_id"],
                 cimeaEuroPrice=context.user_data["cimea_euro_price"], cimeaRial=context.user_data["cimea_rial"],
                 trans_filepath=context.user_data["cimea_trans_filepath"], finish=0)

def reserve_hotel_control(update, context):
    insert_or_update_user(update, context)
    ordersId = insert_and_get_ordersId("reserve_hotel")
    insert_reserve_hotel(context._user_id, ordersId=ordersId, finish=0)

def get_admin_control(update, context):
    result = get_admin_by_tel_userId(context._user_id)
    return len(result)


def get_order_controller_buyEuro(finish):
    data = get_buyEuro_admin(finish)

    formatted_list = [
    (
        f"🆔شناسه خرید:\n{item['buyCurrencyId']}\n\n"
        f"📎شناسه: #سفارش_{item['ordersId']}\n"
        f"📌نوع پرداختی:\nخرید یورو\n"
        f"{'-'*50}\n\n"
        f"⏰زمان:\n{item['time'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"👤نام:\n{item['userFirstName']} {item['userLastName'] if item['userLastName'] else 'نامشخص'}\n\n"
        f"🏷نام کاربری:\n{item['userName']}\n\n"
        f"📞تلفن:\n{item['phoneNumber']}\n\n"
        f"💰مقدار:\n{item['value']}\n\n"
        f"💱ارز:\n{item['currency_name']}\n\n"
        f"result10",
        None  # Second element of the tuple
    )
    for item in data
    ]

    return formatted_list


def get_order_controller_otherOrder(finish):
    data = get_otherOrder_admin(finish)

    formatted_list = [(
        f"🆔شناسه سفارش:\n{item['orderOtherId']}\n\n"
        f"📎شناسه: #سفارش_{item['ordersId']}\n"
        f"📌نوع پرداختی:\nothers\n"
        f"{'-'*50}\n\n"
        f"⏰زمان:\n{item['time'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"👤نام:\n{item['userFirstName']} {item['userLastName'] if item['userLastName'] else 'نامشخص'}\n\n"
        f"🏷نام کاربری:\n{item['userName']}\n\n"
        f"📞تلفن:\n{item['phoneNumber']}\n\n"
        f"📝توضیحات:\n{item['description']}\n\n"
        f"💰قیمت:\n{item['price']}\n\n"
        f"result11",
        None)
        for item in data
    ]

    return formatted_list


def get_order_controller_reserveHotel(finish):
    data = get_reserveHotel_admin(finish)

    formatted_list = [(
        f"🆔شناسه رزرو:\n{item['reserveHotelID']}\n\n"
        f"📎شناسه: #سفارش_{item['ordersId']}\n"
        f"🏨نوع پرداختی:\nرزرو هتل\n"
        f"{'-'*50}\n\n"
        f"⏰زمان:\n{item['time'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"👤نام:\n{item['userFirstName']} {item['userLastName'] if item['userLastName'] else 'نامشخص'}\n\n"
        f"🏷نام کاربری:\n{item['userName']}\n\n"
        f"📞تلفن:\n{item['phoneNumber']}\n\n"
        f"result12",
        None)
        for item in data
    ]
    return formatted_list


def get_order_controller_reguni(finish):
    data = get_regUni_admin(finish)

    formatted_list = [(
        f"🆔شناسه ثبت‌نام:\n{item['regUniId']}\n\n"
        f"📎شناسه: #سفارش_{item['ordersId']}\n"
        f"📌نوع پرداختی:\nثبت‌نام دانشگاه\n"
        f"{'-'*50}\n\n"
        f"⏰زمان:\n{item['time'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"👤نام:\n{item['userFirstName']} {item['userLastName'] if item['userLastName'] else 'نامشخص'}\n\n"
        f"🏷نام کاربری:\n{item['userName']}\n\n"
        f"📞تلفن:\n{item['phoneNumber']}\n\n"
        f"📚نوع ثبت‌نام:\n{item['regTypeName']}\n\n"
        f"🎓مقطع تحصیلی:\n{item['regCourseLevelName']}\n\n"
        f"🗣زبان دوره:\n{item['regCourseLangName']}\n\n"
        f"🏛دانشگاه:\n{item['uniName']}\n\n"
        f"📖نام رشته/دوره:\n{item['courseName']}\n\n"
        f"result13",
        None)
        for item in data
    ]

    return formatted_list


def get_order_controller_tuitionFee(finish):
    data = get_tuitionFee_admin(finish)
    formatted_list = [
        (
            f"🆔شناسه پرداخت شهریه:\n{item['tuitionFeeId']}\n\n"
            f"📎شناسه: #سفارش_{item['ordersId']}\n"
            f"📌نوع پرداختی:\nپرداخت شهریه\n"
            f"{'-'*50}\n\n"
            f"⏰زمان:\n{item['time'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"👤نام:\n{item['userFirstName']} {item['userLastName'] if item['userLastName'] else 'نامشخص'}\n\n"
            f"🏷نام کاربری:\n{item['userName']}\n\n"
            f"📞تلفن:\n{item['phoneNumber']}\n\n"
            f"🏛دانشگاه:\n{item['university']}\n\n"
            f"🎓مدرک تحصیلی:\n{item['degree']}\n\n"
            "result14",
            None
        )
        for item in data
    ]

    return formatted_list


def get_order_controller_cimea(finish):
    data = get_cimea_admin(finish)

    formatted_list = [
    (
        f"🆔شناسه CIMEA:\n{item['cimeaId']}\n\n"
        f"📎شناسه: #سفارش_{item['ordersId']}\n"
        f"📌نوع پرداختی:\nCIMEA\n"
        f"{'-'*50}\n\n"
        f"⏰زمان:\n{item['time'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"👤نام:\n{item['userFirstName']} {item['userLastName'] if item['userLastName'] else 'نامشخص'}\n\n"
        f"🏷نام کاربری:\n{item['userName']}\n\n"
        f"📞تلفن:\n{item['phoneNumber']}\n\n"
        f"💶مقدار یورو:\n{item['cimeaPrice']}\n\n"
        f"💱قیمت یورو:\n{item['cimeaEuroPrice']}\n\n"
        f"💰مبلغ نهایی (تومان):\n{item['cimeaRial']}\n\n"
        f"🚀سرعت بررسی:\n{item['cimeaSpeedName']}\n\n"
        f"📄نوع مقایسه:\n{item['cimeaTypeName']}\n\n"
        f"result15",
        item['trans_filepath'],  # Transaction file in second field of tuple
        "cimea",
        )
        for item in data
    ]

    return formatted_list


def get_order_controller_appFee(finish):
    data = get_appFee_admin(finish)

    formatted_list = [
    (
        f"🆔شناسه پرداخت اپلیکیشن فی:\n{item['appFeeId']}\n\n"
        f"📎شناسه: #سفارش_{item['ordersId']}\n"
        f"📌نوع پرداختی:\nپرداخت اپلیکیشن فی\n"
        f"{'-'*50}\n\n"
        f"⏰زمان:\n{item['time'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"👤نام:\n{item['userFirstName']} {item['userLastName'] if item['userLastName'] else 'نامشخص'}\n\n"
        f"🏷نام کاربری:\n{item['userName']}\n\n"
        f"📞تلفن:\n{item['phoneNumber']}\n\n"
        f"🏛دانشگاه:\n{item['university']}\n\n"
        f"🎓مدرک تحصیلی:\n{item['degree']}\n\n"
        f"💶مقدار یورو:\n{item['euroAmount']}\n\n"
        f"💱قیمت یورو:\n{item['euroPrice']}\n\n"
        f"💰مبلغ نهایی (تومان):\n{item['rialchange']}\n\n"
        f"result16",
        item['trans_filepath'],  # Transaction file in second field of tuple
        "app_and_tuition_fee",
        )
        for item in data
    ]

    return formatted_list


def get_order_controller_tovergata(finish):
    data = get_toevergata_admin(finish)

    formatted_list = [
        (
            f"🆔شناسه پرداخت Tor Vergata:\n{item['torvergataId']}\n\n"
            f"📎شناسه: #سفارش_{item['ordersId']}\n"
            f"📌نوع پرداختی:\nپرداخت Tor Vergata\n"
            f"{'-'*50}\n\n"
            f"⏰زمان:\n{item['time'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"👤نام:\n{item['userFirstName']} {item['userLastName'] if item['userLastName'] else 'نامشخص'}\n\n"
            f"🏷نام کاربری:\n{item['userName']}\n\n"
            f"📞تلفن:\n{item['phoneNumber']}\n\n"
            f"💶مقدار یورو:\n{item['euroAmount']}\n\n"
            f"💱قیمت یورو:\n{item['euroPrice']}\n\n"
            f"💰مبلغ نهایی (تومان):\n{item['rial']}\n\n"
            f"result17",
            item['trans_filepath'],  # Transaction file in second field of tuple
            "torvergata",
        )
        for item in data
    ]

    return formatted_list


def get_order_controller_tolcExam(finish):
    data = get_tolcExam_admin(finish)

    formatted_list = [
    (
        f"🆔شناسه سفارش آزمون TOLC:\n{item['tolcOrderExamId']}\n\n"
        f"📎شناسه: #سفارش_{item['ordersId']}\n"
        f"📌نوع پرداختی:\nسفارش آزمون TOLC\n"
        f"{'-'*50}\n\n"
        f"⏰زمان:\n{item['time'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"👤نام:\n{item['userFirstName']} {item['userLastName'] if item['userLastName'] else 'نامشخص'}\n\n"
        f"🏷نام کاربری:\n{item['userName']}\n\n"
        f"📞تلفن:\n{item['phoneNumber']}\n\n"
        f"📝نام آزمون:\n{item['tolcExamDetailName']}\n\n"
        f"📚نوع آزمون:\n{item['tolcExamTypeName']}\n\n"
        f"🔑نام کاربری چیزآ:\n{item['username']}\n\n"
        f"🔒رمز عبور چیزآ:\n{decrypting_password(item['password'])}\n\n"
        f"💶مقدار یورو:\n{item['euroAmount']}\n\n"
        f"💱قیمت یورو:\n{item['euroPrice']}\n\n"
        f"💰مبلغ نهایی (تومان):\n{item['rial_change']}\n\n"
        f"result18",
        item['trans_filePath'],  # Transaction file in the second field of tuple
        "tolc_exam",
    )
    for item in data
    ]

    return formatted_list



def get_order_controller(finish):
    data=[]
    for i in get_order_controller_buyEuro(finish):
        data.append(i)
    for i in get_order_controller_otherOrder(finish):
        data.append(i)
    for i in get_order_controller_reserveHotel(finish):
        data.append(i)
    for i in get_order_controller_reguni(finish):
        data.append(i)
    for i in get_order_controller_tuitionFee(finish):
        data.append(i)
    for i in get_order_controller_cimea(finish):
        data.append(i)
    for i in get_order_controller_appFee(finish):
        data.append(i)
    for i in get_order_controller_tovergata(finish):
        data.append(i)
    for i in get_order_controller_tolcExam(finish):
        data.append(i)

    return data


def update_isfinish_controller(message, finish):
    id = int(message.split("\n")[1])
    table_id = int(message[-2:])
    
    if table_id == 10 :
        update_finish("buy_currency", finish, "buyCurrencyId", id)
    elif table_id == 11:
        update_finish("order_other", finish, "orderOtherId", id)
    elif table_id == 12:
        update_finish("reserve_hotel", finish, "reserveHotelID", id)
    elif table_id == 13:
        update_finish("reg_uni", finish, "regUniId", id)
    elif table_id == 14:
        update_finish("tuition_fee", finish, "tuitionFeeId", id)
    elif table_id == 15:
        update_finish("cimea", finish, "cimeaId", id)
    elif table_id == 16:
        update_finish("app_fee", finish, "appFeeId", id)
    elif table_id == 17:
        update_finish("torvergata", finish, "torvergataId", id)
    elif table_id == 18:
        update_finish("tolc_order_exam", finish, "tolcOrderExamId", id)