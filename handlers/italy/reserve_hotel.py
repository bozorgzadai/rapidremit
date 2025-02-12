from telegram import Update
from telegram.ext import ContextTypes
from handlers.States import States
from handler import goto_main_menu
from handlers.italy.italy_main import goto_italy
from create_keyboard import back_button_keyboard



async def goto_italy_reserve_hotel_id(update: Update) -> int:
    await update.message.reply_text(
        "کاربر گرامی لطفا آیدی تلگرامی خود را جهت ارتباط ادمین های پرداختی وارد نمایید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_RESERVE_HOTEL_ID

async def italy_reserve_hotel_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        return await goto_italy(update)

    context.user_data["id"] = update.message.text
    return await goto_italy_reserve_hotel_contact(update)
    


async def goto_italy_reserve_hotel_contact(update):
    await update.message.reply_text(
        "کاربر گرامی لطفا شماره تماس خود را جهت پیگیری های آتی برای سفارش خود وارد کنید:",
        reply_markup=back_button_keyboard()
    )
    return States.ITALY_RESERVE_HOTEL_CONTACT

async def italy_reserve_hotel_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "بازگشت":
        return await goto_italy_reserve_hotel_id(update, context)

    context.user_data["contact"] = update.message.text
    message = "ادمین های پرداختی جهت دریافت اطلاعات بیشتر از شما در راستای تکمیل سفارش ارتباط خواهند گرفت."
    return await goto_main_menu(update, context, message)
