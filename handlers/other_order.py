from telegram import Update
from telegram.ext import ContextTypes
from handlers.States import States
from create_keyboard import back_button_keyboard
from handler import goto_main_menu
from controller import other_order_control


async def goto_others(update):
    await update.message.reply_text(
        "لطفا توضیحات سفارش خود را وارد کنید:",
        reply_markup=back_button_keyboard()
    )
    return States.OTHERS_DESCRIPTION

async def others_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_main_menu(update, context)
    
    context.user_data["description"] = text
    return await goto_others_amount(update)
    


async def goto_others_amount(update, message=None):
    default_message = "لطفا مبلغ قابل پرداخت در سفارش را به یورو وارد کنید:"

    if message:
        show_message = message
    else:
        show_message = default_message

    await update.message.reply_text(
        show_message,
        reply_markup=back_button_keyboard()
    )
    return States.OTHERS_AMOUNT

async def others_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_others(update)
    if text.isdigit():
        context.user_data["amount"] = float(text)
        return await goto_others_contact(update)
    else:
        message = "لطفا یک عدد معتبر وارد کنید."
        return await goto_others_amount(update, message)



async def goto_others_contact(update):
    await update.message.reply_text(
        "لطفا شماره تماس خود را وارد کنید:",
        reply_markup=back_button_keyboard()
    )
    return States.OTHERS_CONTACT

async def others_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_others_amount(update)
    
    context.user_data["contact"] = text
    return await goto_others_id(update)
    


async def goto_others_id(update):
    await update.message.reply_text(
        "لطفا آیدی خود را وارد نمایید",
        reply_markup=back_button_keyboard()
    )
    return States.OTHERS_ID

async def others_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text == "بازگشت":
        return await goto_others_contact(update)
    
    context.user_data["id"] = text
    other_order_control(update, context)

    message = "سفارش شما ثبت شد. ادمین به زودی با شما تماس خواهد گرفت."
    return await goto_main_menu(update, context, message)


