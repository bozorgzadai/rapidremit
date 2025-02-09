
from database import Database


def get_reg_type():
    db = Database.get_database()
    select_query = "SELECT * FROM reg_type"
    return  db.select(select_query)

def get_reg_course_level():
    db = Database.get_database()
    select_query = "SELECT * FROM reg_course_level"
    return  db.select(select_query)

def get_reg_course_lang():
    db = Database.get_database()
    select_query = "SELECT * FROM reg_course_lang"
    return  db.select(select_query)

def get_tolc_exam_type():
    db = Database.get_database()
    select_query = "SELECT * FROM tolc_exam_type"
    return  db.select(select_query)



def get_user_by_id(user_id):
    db = Database.get_database()
    select_query = "SELECT * FROM user WHERE tel_userId = %s"
    select_params = (user_id,)
    return db.select(select_query, select_params)

def get_cisia_account_by_tel_userId(tel_userId):
    db = Database.get_database()
    select_query = "SELECT * FROM cisia_account WHERE tel_userId = %s"
    select_params = (tel_userId,)
    return db.select(select_query, select_params)

def get_id_by_regTypeName(regTypeName):
    db = Database.get_database()
    select_query = "SELECT * FROM reg_type WHERE regTypeName = %s"
    select_params = (regTypeName,)
    return db.select(select_query, select_params)

def get_id_by_regCourseLevelName(regCourseLevelName):
    db = Database.get_database()
    select_query = "SELECT * FROM reg_course_level WHERE regCourseLevelName = %s"
    select_params = (regCourseLevelName,)
    return db.select(select_query, select_params)

def get_id_by_regCourseLangName(regCourseLangName):
    db = Database.get_database()
    select_query = "SELECT * FROM reg_course_lang WHERE regCourseLangName = %s"
    select_params = (regCourseLangName,)
    return db.select(select_query, select_params)

def get_id_by_tolcExamTypeName(tolcExamTypeName):
    db = Database.get_database()
    select_query = "SELECT * FROM tolc_exam_type WHERE tolcExamTypeName = %s"
    select_params = (tolcExamTypeName,)
    return db.select(select_query, select_params)

def get_id_by_tolcExamDetailName(tolcExamDetailName):
    db = Database.get_database()
    select_query = "SELECT * FROM tolc_exam_detail WHERE tolcExamDetailName = %s"
    select_params = (tolcExamDetailName,)
    return db.select(select_query, select_params)

def get_tolcExamDetailName_by_tolcExamTypeId(tolcExamTypeId):
    db = Database.get_database()
    select_query = "SELECT * FROM tolc_exam_detail WHERE tolcExamTypeId = %s"
    select_params = (tolcExamTypeId,)
    return db.select(select_query, select_params)




def insert_user(userId, userName='', userFirstName='', userLastName='', phoneNumber='', birthDate='', passport_photo=''):
    db = Database.get_database()
    insert_query = """INSERT INTO user(tel_userId, userName, userFirstName, userLastName, phoneNumber, birthDate, passport_photo)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    insert_params = (userId, userName, userFirstName, userLastName, phoneNumber, birthDate, passport_photo)
    db.execute(insert_query, insert_params)


def insert_buy_currency(tel_userId, currencyId, value=''):
    db = Database.get_database()
    insert_query = """INSERT INTO buy_currency(tel_userId, currencyId, value)
                                    VALUES (%s, %s, %s)"""
    insert_params = (tel_userId, currencyId, value)
    db.execute(insert_query, insert_params)


def insert_other_order(tel_userId, description='', price='', finish=''):
    db = Database.get_database()
    insert_query = """INSERT INTO order_other(tel_userId, description, price, finish)
                                    VALUES (%s, %s, %s, %s)"""
    insert_params = (tel_userId, description, price, finish)
    db.execute(insert_query, insert_params)


def insert_app_fee(tel_userId, university='', degree='', euroAmount='', euroPrice='', rialChange='', trans_filepath='', finish=''):
    db = Database.get_database()
    insert_query = """INSERT INTO app_fee(tel_userId, university, degree, euroAmount, euroPrice, rialChange, trans_filepath, finish)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    insert_params = (tel_userId, university, degree, euroAmount, euroPrice, rialChange, trans_filepath, finish)
    db.execute(insert_query, insert_params)


def insert_tuition_fee(tel_userId, university='', degree='', euroAmount='', euroPrice='', rialChange='', trans_filepath='', finish=''):
    db = Database.get_database()
    insert_query = """INSERT INTO tuition_fee(tel_userId, university, degree, euroAmount, euroPrice, rial_change, trans_filepath, finish)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    insert_params = (tel_userId, university, degree, euroAmount, euroPrice, rialChange, trans_filepath, finish)
    db.execute(insert_query, insert_params)


def insert_reg_uni(tel_userId, regTypeId='', regCourseLevelId='', regCourseLangId='', uniName='', courseName='', finish=''):
    db = Database.get_database()
    insert_query = """INSERT INTO reg_uni(tel_userId, regTypeId, regCourseLevelId, regCourseLangId, uniName, courseName, finish)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    insert_params = (tel_userId, regTypeId, regCourseLevelId, regCourseLangId, uniName, courseName, finish)
    db.execute(insert_query, insert_params)


def insert_tolc_order_exam(tel_userId, tolcExamDetailId='', examDate='', trans_filePath='', finish=''):
    db = Database.get_database()
    insert_query = """INSERT INTO tolc_order_exam(tel_userId, tolcExamDetailId, examDate, trans_filePath, finish)
                                    VALUES (%s, %s, %s, %s, %s)"""
    insert_params = (tel_userId, tolcExamDetailId, examDate, trans_filePath, finish)
    db.execute(insert_query, insert_params)


def insert_cisia_account(tel_userId, username='', password=''):
    db = Database.get_database()
    insert_query = """INSERT INTO cisia_account(tel_userId, username, password)
                                    VALUES (%s, %s, %s)"""
    insert_params = (tel_userId, username, password)
    db.execute(insert_query, insert_params)




def update_user(userId, userName='', userFirstName='', userLastName='', phoneNumber='', birthDate='', passport_photo=''):
    db = Database.get_database()
    update_query = """ UPDATE user SET userName=%s, userFirstName=%s, userLastName=%s, phoneNumber=%s, birthDate=%s, passport_photo=%s
                                        WHERE tel_userId = %s"""
    update_params = (userName, userFirstName, userLastName, phoneNumber, birthDate, passport_photo, userId)
    db.execute(update_query, update_params)


def update_cisia_account(tel_userId, username='', password=''):
    db = Database.get_database()
    
    update_query = """ UPDATE cisia_account SET username=%s, password=%s
                                        WHERE tel_userId = %s"""
    update_params = (tel_userId, username, password)
    db.execute(update_query, update_params)

