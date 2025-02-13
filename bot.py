from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, filters
from BotStates import States, AdminStates
from config import TOKEN
from utils import terminate_handler
from handlers.admin.admin_menu import admin_menu, goto_admin_menu
from handlers.admin.broadcast_message import broadcast
from handlers.main_menu import  main_menu, goto_main_menu
from handlers.buy_euro import buy_euro_amount, buy_euro_contact, buy_euro_id
from handlers.other_order import others_description, others_amount, others_contact, others_id
from handlers.italy.italy_main import italy
from handlers.italy.exam.exam_main import italy_reserve_exam
from handlers.italy.reserve_hotel import italy_reserve_hotel_id, italy_reserve_hotel_contact

from handlers.italy.cimea import (italy_cimea_receive_phone, italy_cimea_receive_tg_id, italy_cimea,
                                  italy_cimea_receipt, italy_cimea_confirm, italy_cimea_speed,)

from handlers.italy.app_tuition_fee import (italy_app_fee_uni, italy_app_fee_degree, italy_app_fee_tgid, italy_app_fee_contact,
                                            italy_app_fee_amount, italy_app_fee_confirm, italy_app_fee_receipt,)

from handlers.italy.register_uni import (italy_register_university_name, italy_register_university_type, italy_register_university_course,
                                         italy_register_university_degree, italy_register_university_language,
                                         italy_register_university_tgid, italy_register_university_contact,)

from handlers.italy.exam.torvergata import (reserve_torvergata, reserve_torvergata_id, reserve_torvergata_contact,
                                            handle_payment_receipt,)

from handlers.italy.exam.tolc import (italy_reserve_exam_tolc, handle_iolc_x_selection, have_cisia_account, get_cisia_username,
                                      get_cisia_pass, get_exam_date, get_id, get_phone, confirm_payment, payment)

from handlers.admin.isfinish_order import isfinish_order


def main():
    print("Bot is starting...")
    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', goto_main_menu)],
        states={
            States.MAIN_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu)
            ],



            States.BUY_EURO_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, buy_euro_amount)
            ],
            States.BUY_EURO_CONTACT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, buy_euro_contact)
            ],
            States.BUY_EURO_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, buy_euro_id)
            ],



            States.OTHERS_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, others_description)
            ],
            States.OTHERS_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, others_amount)
            ],
            States.OTHERS_CONTACT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, others_contact)
            ],
            States.OTHERS_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, others_id)
            ],



            States.HAVE_CISIA_ACCOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, have_cisia_account)
            ],
            States.GET_CISIA_USERNAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_cisia_username)
            ],
            States.GET_CISIA_PASS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_cisia_pass)
            ],
            States.GET_EXAM_DATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_exam_date)
            ],
            States.GET_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_id)
            ],
            States.GET_PHONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)
            ],
            States.CONFIRM_PAYMENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_payment)
            ],
            States.PAYMENT: [
                MessageHandler(filters.PHOTO & ~filters.COMMAND, payment),
                MessageHandler(filters.TEXT & ~filters.COMMAND, payment)
            ],



            States.ITALY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy)
            ],
            States.ITALY_RESERVE_EXAM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_reserve_exam)
            ],
            States.ITALY_RESERVE_EXAM_TOLC: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_reserve_exam_tolc)
            ],
            States.ITALY_RESERVE_EXAM_TOLC_X: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_iolc_x_selection)
            ],



            States.ITALY_CIMEA: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_cimea)
            ],
            States.ITALY_CIMEA_SPEED: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_cimea_speed)
            ],
            States.ITALY_CIMEA_CONFIRM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_cimea_confirm)
            ],
            States.ITALY_CIMEA_RECEIPT_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_cimea_receive_tg_id)
            ],
            States.ITALY_CIMEA_RECEIPT_PHONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_cimea_receive_phone)
            ],
            States.ITALY_CIMEA_RECEIPT: [
                MessageHandler(filters.PHOTO & ~filters.COMMAND, italy_cimea_receipt),
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_cimea_receipt),
            ],



            States.ITALY_APP_FEE_UNI: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_app_fee_uni),
            ],
            States.ITALY_APP_FEE_DEGREE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_app_fee_degree),
            ],
            States.ITALY_APP_FEE_TGID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_app_fee_tgid),
            ],
            States.ITALY_APP_FEE_CONTACT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_app_fee_contact),
            ],
            States.ITALY_APP_FEE_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_app_fee_amount),
            ],
            States.ITALY_APP_FEE_CONFIRM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_app_fee_confirm),
            ],
            States.ITALY_APP_FEE_RECEIPT: [
                MessageHandler(filters.PHOTO & ~filters.COMMAND, italy_app_fee_receipt),
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_app_fee_receipt),
            ],



            States.ITALY_RESERVE_HOTEL_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_reserve_hotel_id)
            ],
            States.ITALY_RESERVE_HOTEL_CONTACT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_reserve_hotel_contact)
            ],

            

            States.ITALY_REGISTER_UNIVERSITY_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_register_university_name)
            ],
            States.ITALY_REGISTER_UNIVERSITY_TYPE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_register_university_type)
            ],
            States.ITALY_REGISTER_UNIVERSITY_COURSE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_register_university_course)
            ],
            States.ITALY_REGISTER_UNIVERSITY_DEGREE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_register_university_degree)
            ],
            States.ITALY_REGISTER_UNIVERSITY_LANGUAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_register_university_language)
            ],
            States.ITALY_REGISTER_UNIVERSITY_TGID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_register_university_tgid)
            ],
            States.ITALY_REGISTER_UNIVERSITY_CONTACT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, italy_register_university_contact)
            ],



            States.torvergata: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, reserve_torvergata)
            ],
            States.torvergata_ID : [
                MessageHandler(filters.TEXT & ~filters.COMMAND, reserve_torvergata_id)
            ],
            States.torvergata_CONTACT : [
                MessageHandler(filters.TEXT & ~filters.COMMAND, reserve_torvergata_contact)
            ],
            States.WAITING_FOR_PAYMENT: [
                MessageHandler(filters.PHOTO & ~filters.COMMAND, handle_payment_receipt),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_payment_receipt),
            ],

        },
        fallbacks=[MessageHandler(filters.COMMAND, terminate_handler),],
        allow_reentry=True,
    )
    application.add_handler(conv_handler, group=1)




    admin_handler = ConversationHandler(
        entry_points=[CommandHandler('admin', goto_admin_menu)],
        states={
            AdminStates.ADMIN_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, admin_menu)
            ],
            AdminStates.ISFINISH_ORDER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, isfinish_order)
            ],
            AdminStates.BROADCAST: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, broadcast)
            ],


        },
        fallbacks=[MessageHandler(filters.COMMAND, terminate_handler),],
        allow_reentry=True,
    )
    application.add_handler(admin_handler, group=2)



    # Error handler
    async def error_handler(update: object, context) -> None:
        print(f'Error: {context.error}')
        if update:
            if hasattr(update, "message") and update.message:
                await update.message.reply_text(
                    "An unexpected error occurred. Please try again later."
                )

    application.add_error_handler(error_handler)
    application.run_polling()


if __name__ == '__main__':
    main()

