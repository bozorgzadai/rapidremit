from telegram import Update
from telegram.ext import ContextTypes
from BotStates import States
from handlers.main_menu import goto_main_menu
from utils import save_transaction_image
from handlers.italy.exam.exam_main import goto_italy_reserve_exam
from create_keyboard import back_button_keyboard, pay_cancel_keyboard
from controller import torvergata_control
from utils import get_euro_to_toman_exchange_rate_api, save_transaction_image




async def goto_reserve_torvergata_id(update):
    await update.message.reply_text(
        "لطفا آیدی خود را وارد نمایید",
        reply_markup=back_button_keyboard()
    )
    return States.torvergata_ID

async def reserve_torvergata_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_italy_reserve_exam(update)

    context.user_data["id"] = text
    return await goto_reserve_torvergata_contact(update)
    


async def goto_reserve_torvergata_contact(update):
    await update.message.reply_text(
        "لطفا شماره تلفن خود را جهت ارتباطات بعدی وارد کنید:",
        reply_markup=back_button_keyboard()
    )
    return States.torvergata_CONTACT

async def reserve_torvergata_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_reserve_torvergata_id(update)
    
    context.user_data["contact"] = text
    return await goto_reserve_torvergata(update)

    

async def goto_reserve_torvergata(update, message=None):
    torvergata_euro_amount= 32
    euro_price, unit = await get_euro_to_toman_exchange_rate_api()
    amount_rial = int(torvergata_euro_amount  * euro_price + 480000)



    default_message = f"داوطلب گرامی هزینه شرکت در آزمون داروسازی تورورگاتا (کورس انگلیسی داروسازی) {amount_rial} تومان می‌باشد اگر قصد تکمیل خرید خود را دارید با استفاده از گزینه پرداخت ادامه دهید"

    if message:
        show_message = message
    else:
        show_message = default_message

    await update.message.reply_text(
        show_message,
        reply_markup=pay_cancel_keyboard()
    )
    return States.torvergata

async def reserve_torvergata(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_reserve_torvergata_contact(update)
    elif text == "انصراف":
        return await goto_main_menu(update, context)
    elif text == "پرداخت":
        return await goto_handle_payment_receipt(update)
    else: 
        message = "لطفا یکی از گزینه‌های زیر را انتخاب کنید:"
        return await goto_reserve_torvergata(update, message)



async def goto_handle_payment_receipt(update, message=None):
    card_number = "5022-2913-3054-7298\nنیما فتوکیان"

    default_message = f"""لطفا جهت پرداخت هزینه مبلغ مذکور را به شماره کارت\n {card_number}\n واریز نمایید.\n
سپس فیش پرداختی خود را در همین ربات ارسال کنید (عکس فیش را بفرستید)."""

    if message:
        show_message = message
    else:
        show_message = default_message

    await update.message.reply_text(
        show_message,
        reply_markup=back_button_keyboard()
    )
    return States.WAITING_FOR_PAYMENT

async def handle_payment_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.photo:
        save_directory = "saved_photo/torvergata"
        filename = await save_transaction_image(update, context, save_directory)
        context.user_data["torvergata_trans_filepath"] = filename

        torvergata_control(update, context)

        message = "کاربر گرامی، درخواست شما با موفقیت ثبت شد. ادمین‌های پرداختی ما در سریع‌ترین فرصت با شما ارتباط خواهند گرفت."
        return await goto_main_menu(update, context, message)
    
    elif update.message.text=="بازگشت":
        return await goto_reserve_torvergata(update)
    
    else:
        message = "لطفا یک تصویر از فیش پرداختی خود ارسال کنید."
        return await goto_handle_payment_receipt(update, message)
