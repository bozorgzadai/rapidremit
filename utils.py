
from telegram.ext import ConversationHandler
import os
import time
import aiohttp


async def terminate_handler(update, context):
    """
    Terminate the current conversation when a command is received.
    """
    return ConversationHandler.END



# Asynchronous function to get the Euro to Iranian Toman exchange rate from the URL
async def get_euro_to_toman_exchange_rate_api(url="https://brsapi.ir/FreeTsetmcBourseApi/Api_Free_Gold_Currency.json"):
    try:
        # Use aiohttp to send an asynchronous GET request
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # Check if the request was successful (status code 200)
                if response.status == 200:
                    # Parse the JSON data
                    data = await response.json()
                    
                    # Iterate over the 'currency' list to find the Euro exchange rate
                    for currency in data.get("currency", []):
                        if currency.get("name") == "یورو":
                            return currency.get("price"), currency.get("unit")
                
                else:
                    print(f"Failed to fetch data. Status code: {response.status}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return None, None




async def save_transaction_image(update, context, save_directory):
    # Get the largest version of the photo (last item in the list)
    photo_file = await update.message.photo[-1].get_file()

    os.makedirs(save_directory, exist_ok=True)

    # Generate a unique file name using timestamp and user ID
    user_id = context._user_id  # Get the Telegram user ID
    # user_id = update.message.from_user.id  # Get the Telegram user ID
    timestamp = int(time.time() * 1000)  # Current time in milliseconds
    unique_filename = f"{user_id}_{timestamp}.jpg"

    # Define the path where you want to save the photo
    file_path = os.path.join(save_directory, unique_filename)

    # Download and save the photo
    await photo_file.download_to_drive(custom_path=file_path)

    return unique_filename



async def send_image(update, context, image_path) -> None:
    chat_id = update.message.chat_id

    if os.path.exists(image_path):  # Ensure the file exists
        with open(image_path, 'rb') as photo:
            await context.bot.send_photo(chat_id=chat_id, photo=photo)
    else:
        await update.message.reply_text("Image not found on the server.")