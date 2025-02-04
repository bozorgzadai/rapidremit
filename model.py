
from database import Database

def get_reg_type():
    db = Database.get_database()
    select_query = "SELECT * FROM reg_type"
    return  db.select(select_query)


def get_reg_course_level():
    db = Database.get_database()
    select_query = "SELECT * FROM reg_course_level"
    return  db.select(select_query)