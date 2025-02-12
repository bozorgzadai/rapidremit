from enum import Enum, auto

class States(Enum):
    MAIN_MENU = auto()

    BUY_EURO_AMOUNT = auto()
    BUY_EURO_CONTACT = auto()
    BUY_EURO_ID = auto()

    OTHERS_DESCRIPTION = auto()
    OTHERS_AMOUNT = auto()
    OTHERS_CONTACT = auto()
    OTHERS_ID = auto()

    ITALY = auto()
    ITALY_RESERVE_EXAM = auto()
    ITALY_RESERVE_EXAM_TOLC = auto()
    ITALY_RESERVE_EXAM_TOLC_X = auto()

    ITALY_CIMEA = auto()
    ITALY_CIMEA_SPEED = auto()
    ITALY_CIMEA_CONFIRM = auto()
    ITALY_CIMEA_RECEIPT = auto()

    torvergata = auto()
    torvergata_ID = auto()
    torvergata_CONTACT = auto()
    WAITING_FOR_PAYMENT = auto()

    ITALY_APP_FEE_UNI = auto()
    ITALY_APP_FEE_DEGREE = auto()
    ITALY_APP_FEE_TGID = auto()
    ITALY_APP_FEE_CONTACT = auto()
    ITALY_APP_FEE_AMOUNT = auto()
    ITALY_APP_FEE_CONFIRM = auto()
    ITALY_APP_FEE_RECEIPT = auto()
    
    ITALY_RESERVE_HOTEL_ID = auto() 
    ITALY_RESERVE_HOTEL_CONTACT = auto()

    ITALY_REGISTER_UNIVERSITY_NAME = auto() 
    ITALY_REGISTER_UNIVERSITY_TYPE = auto()  
    ITALY_REGISTER_UNIVERSITY_COURSE = auto() 
    ITALY_REGISTER_UNIVERSITY_DEGREE = auto()  
    ITALY_REGISTER_UNIVERSITY_LANGUAGE = auto()
    ITALY_REGISTER_UNIVERSITY_TGID = auto() 
    ITALY_REGISTER_UNIVERSITY_CONTACT = auto()

    ITALY_CIMEA_RECEIPT_ID = auto()
    ITALY_CIMEA_RECEIPT_PHONE = auto()

    HAVE_CISIA_ACCOUNT = auto()
    GET_CISIA_USERNAME = auto()
    GET_CISIA_PASS = auto()
    GET_EXAM_DATE = auto()
    GET_ID = auto()
    GET_PHONE = auto()
    CONFIRM_PAYMENT = auto()
    PAYMENT = auto()
