
import aiohttp
import asyncio

# URL of the API
url = "https://brsapi.ir/FreeTsetmcBourseApi/Api_Free_Gold_Currency.json"

# Asynchronous function to get the Euro to Iranian Toman exchange rate from the URL
async def get_euro_to_toman_exchange_rate():
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





# import requests
# # URL of the API
# url = "https://brsapi.ir/FreeTsetmcBourseApi/Api_Free_Gold_Currency.json"

# # Function to get the Euro to Iranian Toman exchange rate from the URL
# def get_euro_to_toman_exchange_rate():
#     try:
#         # Send a GET request to the URL
#         response = requests.get(url)
        
#         # Check if the request was successful (status code 200)
#         if response.status_code == 200:
#             # Parse the JSON data
#             data = response.json()
            
#             # Iterate over the 'currency' list to find the Euro exchange rate
#             for currency in data.get("currency", []):
#                 if currency.get("name") == "یورو":
#                     return currency.get("price"), currency.get("unit")
        
#         else:
#             print(f"Failed to fetch data. Status code: {response.status_code}")
    
#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")
    
#     return None, None


# # Get the exchange rate
# euro_price, unit = get_euro_to_toman_exchange_rate(url)

# if euro_price:
#     print(f"1 Euro (EUR) = {euro_price} {unit}")
# else:
#     print("Exchange rate for Euro not found.")