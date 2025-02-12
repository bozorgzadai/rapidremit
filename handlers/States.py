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
    ITALY_APP_FEE = auto()
    ITALY_RESERVE_HOTEL = auto()
    ITALY_REGISTER_UNIVERSITY = auto()
    TAKMIL_ORDER_NUMBER = auto()
    TAKMIL_AMOUNT = auto()
    TAKMIL_RECEIPT = auto()
    torvergata = auto()
    torvergata_ID = auto()
    torvergata_CONTACT = auto()

    ITALY_RESERVE_EXAM_CISIA_ACCOUNT = auto()  # بررسی اکانت CISIA
    ITALY_RESERVE_EXAM_DATE = auto()  # وارد کردن روز آزمون
    ITALY_RESERVE_EXAM_TGID = auto()  # وارد کردن آیدی تلگرام
    ITALY_RESERVE_EXAM_PHONE = auto()  # وارد کردن شماره تلفن
    ITALY_RESERVE_EXAM_PAYMENT = auto()  # تایید پرداخت
    ITALY_RESERVE_EXAM_RECEIPT = auto()  # دریافت فیش پرداخت

    
    # حالات جدید مربوط به اپ فی
    ITALY_APP_FEE_UNI = auto()
    ITALY_APP_FEE_DEGREE = auto()
    ITALY_APP_FEE_TGID = auto()
    ITALY_APP_FEE_CONTACT = auto()
    ITALY_APP_FEE_AMOUNT = auto()
    ITALY_APP_FEE_CONFIRM = auto()
    ITALY_APP_FEE_RECEIPT = auto()
    
    # اضافه کردن حالت جدید برای مدیریت فیش پرداخت
    WAITING_FOR_PAYMENT = auto()

    ITALY_RESERVE_HOTEL_ID = auto()  # وارد کردن آیدی تلگرام برای رزرو هتل و هواپیما
    ITALY_RESERVE_HOTEL_CONTACT = auto()  # وارد کردن شماره تماس برای رزرو هتل و هواپیما

    # حالات جدید برای ثبت نام دانشگاه
    ITALY_REGISTER_UNIVERSITY_NAME = auto()  # وارد کردن نام دانشگاه
    ITALY_REGISTER_UNIVERSITY_TYPE = auto()  # انتخاب نوع درخواست (apply/enrollment)
    ITALY_REGISTER_UNIVERSITY_COURSE = auto()  # انتخاب نام کورس
    ITALY_REGISTER_UNIVERSITY_DEGREE = auto()  # انتخاب مقطع کورس
    ITALY_REGISTER_UNIVERSITY_LANGUAGE = auto()  # انتخاب زبان کورس
    ITALY_REGISTER_UNIVERSITY_TGID = auto()  # وارد کردن آیدی تلگرام
    ITALY_REGISTER_UNIVERSITY_CONTACT = auto()  # وارد کردن شماره تماس

    ITALY_CIMEA_RECEIPT_ID = auto()
    ITALY_CIMEA_RECEIPT_PHONE = auto()

    ITALY_RESERVE_EXAM_TOLC_PASS2 = auto()
    ITALY_RESERVE_EXAM_TOLC_PASS = auto()


    HAVE_CISIA_ACCOUNT = auto()
    GET_CISIA_USERNAME = auto()
    GET_CISIA_PASS = auto()
    GET_EXAM_DATE = auto()
    GET_ID = auto()
    GET_PHONE = auto()
    CONFIRM_PAYMENT = auto()
    PAYMENT = auto()
