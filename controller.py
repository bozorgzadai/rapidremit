from database import Database


def get_user_by_id(user_id):
    db = Database.get_database()
    select_query = "SELECT * FROM user WHERE tel_userId = %s"
    select_params = (user_id,)
    return db.select(select_query, select_params)


def insert_user(userId, userName='', userFirstName='', userLastName='', phoneNumber='', birthDate='', passport_photo=''):
    db = Database.get_database()
    insert_query = """INSERT INTO user(tel_userId, userName, userFirstName, userLastName, phoneNumber, birthDate, passport_photo)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    insert_params = (userId, userName, userFirstName, userLastName, phoneNumber, birthDate, passport_photo)
    db.execute(insert_query, insert_params)


def update_user(userId, userName='', userFirstName='', userLastName='', phoneNumber='', birthDate='', passport_photo=''):
    db = Database.get_database()
    update_query = """ UPDATE user SET userName=%s,userFirstName=%s,userLastName=%s,phoneNumber=%s,birthDate=%s,passport_photo=%s
                                        WHERE tel_userId = %s"""
    update_params = (userName, userFirstName, userLastName, phoneNumber, birthDate, passport_photo, userId)
    db.execute(update_query, update_params)


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