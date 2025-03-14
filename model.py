
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

def get_cimea_type():
    db = Database.get_database()
    select_query = "SELECT * FROM cimea_type"
    return  db.select(select_query)

def get_cimea_speed():
    db = Database.get_database()
    select_query = "SELECT * FROM cimea_speed"
    return  db.select(select_query)

def get_telUserId():
    db = Database.get_database()
    select_query = "SELECT tel_userId FROM user"
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

def get_id_by_cimeaTypeName(cimeaTypeName):
    db = Database.get_database()
    select_query = "SELECT * FROM cimea_type WHERE cimeaTypeName = %s"
    select_params = (cimeaTypeName,)
    return db.select(select_query, select_params)

def get_id_by_cimeaSpeedName(cimeaSpeedName):
    db = Database.get_database()
    select_query = "SELECT * FROM cimea_speed WHERE cimeaSpeedName = %s"
    select_params = (cimeaSpeedName,)
    return db.select(select_query, select_params)

def get_cimeaPrice_by_cimeaTypeAndSpeedId(cimeaTypeId, cimeaSpeedId):
    db = Database.get_database()
    select_query = "SELECT * FROM cimea_price WHERE cimeaTypeId = %s AND cimeaSpeedId = %s"
    select_params = (cimeaTypeId, cimeaSpeedId,)
    return db.select(select_query, select_params)

def get_admin_by_tel_userId(tel_userId):
    db = Database.get_database()
    select_query = "SELECT * FROM admin WHERE tel_userId = %s"
    select_params = (tel_userId,)
    return db.select(select_query, select_params)




def get_buyEuro_admin(finish):
    db = Database.get_database()
    select_query = """
        SELECT 
            bc.buyCurrencyId, bc.time, bc.value, 
            u.userFirstName, u.userLastName, u.userName, u.phoneNumber, 
            c.currency_name 
        FROM buy_currency AS bc
        INNER JOIN user AS u ON bc.tel_userId = u.tel_userId
        INNER JOIN currency AS c ON bc.currencyId = c.currency_id
        WHERE bc.finish = %s;
    """
    select_params = (finish,)
    return db.select(select_query, select_params)


def get_otherOrder_admin(finish):
    db = Database.get_database()
    select_query = """
        SELECT 
            o.orderOtherId, 
            u.userFirstName, 
            u.userLastName, 
            u.userName, 
            u.phoneNumber, 
            o.description, 
            o.time, 
            o.price 
        FROM order_other AS o
        INNER JOIN user AS u ON o.tel_userId = u.tel_userId
        WHERE o.finish = %s;
    """
    select_params = (finish,)
    return db.select(select_query, select_params)

def get_reserveHotel_admin(finish):
    db = Database.get_database()
    select_query = """
        SELECT 
            o.reserveHotelID, 
            u.userFirstName, 
            u.userLastName, 
            u.userName, 
            u.phoneNumber, 
            o.time
        FROM reserve_hotel AS o
        INNER JOIN user AS u ON o.tel_userId = u.tel_userId
        WHERE o.finish = %s;
    """
    select_params = (finish,)
    return db.select(select_query, select_params)

def get_regUni_admin(finish):
    db = Database.get_database()
    select_query = """
        SELECT 
            ru.regUniId,
            u.userFirstName, 
            u.userLastName, 
            u.userName, 
            u.phoneNumber, 
            rt.regTypeName,
            rcl.regCourseLevelName,
            rcll.regCourseLangName,
            ru.uniName,
            ru.courseName,
            ru.time
        FROM reg_uni AS ru
        INNER JOIN user AS u ON ru.tel_userId = u.tel_userId
        INNER JOIN reg_type AS rt ON ru.regTypeId = rt.regTypeId
        INNER JOIN reg_course_level AS rcl ON ru.regCourseLevelId = rcl.regCourseLevelId
        INNER JOIN reg_course_lang AS rcll ON ru.regCourseLangId = rcll.regCourseLangId
        WHERE ru.finish = %s;

    """
    select_params = (finish,)
    return db.select(select_query, select_params)



def get_tuitionFee_admin(finish):
    db = Database.get_database()
    select_query = """
        SELECT tf.tuitionFeeId,u.userFirstName, 
                    u.userLastName, 
                    u.userName, 
                    u.phoneNumber,
                    university,
                    degree,
                    time
        FROM tuition_fee tf inner join user u on tf.tel_userId = u.tel_userId 
        where finish=%s;
    """
    select_params = (finish,)
    return db.select(select_query, select_params)


def get_cimea_admin(finish):
    db = Database.get_database()
    select_query = """
        SELECT 
            c.cimeaId, 
            u.userFirstName, 
            u.userLastName, 
            u.userName, 
            u.phoneNumber, 
            cp.cimeaPrice, 
            c.cimeaEuroPrice, 
            c.cimeaRial, 
            c.trans_filepath, 
            c.time, 
            cpi.cimeaSpeedName, 
            ct.cimeaTypeName
        FROM cimea c
        INNER JOIN user u ON u.tel_userId = c.tel_userId
        INNER JOIN cimea_price cp ON cp.cimeaPriceId = c.cimeaPriceId
        INNER JOIN cimea_type ct ON ct.cimeaTypeid = cp.cimeaTypeId
        INNER JOIN cimea_speed cpi ON cpi.cimeaSpeedId = cp.cimeaSpeedId
        WHERE c.finish = %s;
    """
    select_params = (finish,)
    return db.select(select_query, select_params)


def get_appFee_admin(finish):
    db = Database.get_database()
    select_query = """
        SELECT tf.appFeeId,u.userFirstName, 
                    u.userLastName, 
                    u.userName, 
                    u.phoneNumber,
                    university,
                    degree,
                    euroAmount,
                    euroPrice,
                    rialchange,
                    trans_filepath,
                    time
        FROM app_fee tf inner join user u on tf.tel_userId = u.tel_userId 
        where finish=%s;
    """
    select_params = (finish,)
    return db.select(select_query, select_params)

def get_toevergata_admin(finish):
    db = Database.get_database()
    select_query = """
        SELECT 
            t.torvergataId, 
            u.userFirstName, 
            u.userLastName, 
            u.userName, 
            u.phoneNumber, 
            t.trans_filepath, 
            t.time
        FROM torvergata t
        INNER JOIN user u ON t.tel_userId = u.tel_userId
        WHERE t.finish = %s;
    """
    select_params = (finish,)
    return db.select(select_query, select_params)

def get_tolcExam_admin(finish):
    db = Database.get_database()
    select_query = """
    SELECT 
        toe.tolcOrderExamId,
        u.userFirstName, 
        u.userLastName, 
        u.userName, 
        u.phoneNumber,
        ted.tolcExamDetailName,
        tet.tolcExamTypeName,
        toe.trans_filePath,
        toe.time,
        ca.username,
        ca.password
    FROM tolc_order_exam toe
    INNER JOIN user u ON toe.tel_userId = u.tel_userId
    INNER JOIN tolc_exam_detail ted ON ted.tolcExamDetailId = toe.tolcExamDetailId
    INNER JOIN tolc_exam_type tet ON tet.tolcExamTypeId = ted.tolcExamTypeId
    INNER JOIN cisia_account ca ON ca.tel_userId = u.tel_userId
    where toe.finish=%s;
    """
    select_params = (finish,)
    return db.select(select_query, select_params)










def insert_user(userId, userName='', userFirstName='', userLastName='', phoneNumber='', birthDate='', passport_photo=''):
    db = Database.get_database()
    insert_query = """INSERT INTO user(tel_userId, userName, userFirstName, userLastName, phoneNumber, birthDate, passport_photo)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    insert_params = (userId, userName, userFirstName, userLastName, phoneNumber, birthDate, passport_photo)
    db.execute(insert_query, insert_params)


def insert_buy_currency(tel_userId, currencyId, value='', finish=''):
    db = Database.get_database()
    insert_query = """INSERT INTO buy_currency(tel_userId, currencyId, value, finish)
                                    VALUES (%s, %s, %s, %s)"""
    insert_params = (tel_userId, currencyId, value, finish)
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

def insert_tuition_fee(tel_userId, university='', degree='', finish=''):
    db = Database.get_database()
    insert_query = """INSERT INTO tuition_fee(tel_userId, university, degree, finish)
                                    VALUES (%s, %s, %s, %s)"""
    insert_params = (tel_userId, university, degree, finish)
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


def insert_torvergata(tel_userId, trans_filepath='', finish=''):
    db = Database.get_database()
    insert_query = """INSERT INTO torvergata(tel_userId, trans_filepath, finish)
                                    VALUES (%s, %s, %s)"""
    insert_params = (tel_userId, trans_filepath, finish)
    db.execute(insert_query, insert_params)


def insert_cimea(tel_userId, cimeaPriceId='', cimeaEuroPrice='', cimeaRial='', trans_filepath='', finish=''):
    db = Database.get_database()
    insert_query = """INSERT INTO cimea(tel_userId, cimeaPriceId, cimeaEuroPrice, cimeaRial, trans_filepath, finish)
                                    VALUES (%s, %s, %s, %s, %s, %s)"""
    insert_params = (tel_userId, cimeaPriceId, cimeaEuroPrice, cimeaRial, trans_filepath, finish)
    db.execute(insert_query, insert_params)


def insert_reserve_hotel(tel_userId, finish=''):
    db = Database.get_database()
    insert_query = """INSERT INTO reserve_hotel(tel_userId, finish)
                                    VALUES (%s, %s)"""
    insert_params = (tel_userId, finish)
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



def update_finish(table_name,finish,column_name,id):
    db = Database.get_database()

    update_query = f"""
        UPDATE {table_name}
        Set finish = %s
        where {column_name} = %s; 
    """
    update_params = (finish,id)
    db.execute(update_query,update_params)
