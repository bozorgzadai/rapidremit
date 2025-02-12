from telegram import Update
from telegram.ext import ContextTypes
from handlers.States import States
from create_keyboard import back_button_keyboard
from handler import goto_main_menu
from controller import buy_euro_control



async def goto_buy_euro(update, message=None):
    default_message = "لطفا مبلغی که نیاز به ترانسفر آن به حساب بانکی خود دارید به یورو وارد نمایید:"

    if message:
        show_message = message
    else:
        show_message = default_message

    await update.message.reply_text(
        show_message,
        reply_markup=back_button_keyboard()
    )
    return States.BUY_EURO_AMOUNT

async def buy_euro_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_main_menu(update, context)
    if text.isdigit():
        context.user_data["amount"] = float(text)
        return await goto_buy_euro_contact(update)
    else:
        message = "لطفا یک عدد معتبر وارد کنید."
        goto_buy_euro(update, message)



async def goto_buy_euro_contact(update):
    await update.message.reply_text(
        "لطفا شماره خود را جهت ارتباطات بعدی وارد کنید:",
        reply_markup=back_button_keyboard()
    )
    return States.BUY_EURO_CONTACT

async def buy_euro_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_buy_euro(update)

    context.user_data["contact"] = text
    return await goto_buy_euro_id(update)
    


async def goto_buy_euro_id(update):
    await update.message.reply_text(
        "لطفا آیدی خود را وارد کنید",
        reply_markup=back_button_keyboard()
    )
    return States.BUY_EURO_ID
    
async def buy_euro_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        goto_buy_euro_contact(update)

    context.user_data["id"] = text
    buy_euro_control(update, context)

    message = "ادمین‌های پرداختی حوزه خرید یورو و تبدیل ارز در سریع‌ترین حالت با شما جهت اقدامات تکمیلی ارتباط خواهند گرفت."
    return await goto_main_menu(update, context, message)

