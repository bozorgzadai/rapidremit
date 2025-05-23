# RapidRemit Telegram Bot

A Telegram bot built using Python and MySQL to handle user interactions, and service requests. Powered by the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot ) library.

---

## 🧩 Features

- User-friendly menu navigation
- Supports custom orders
- Specific services:
  - Exam reservations
  - University registration
  - Application payments
  - Hotel reservations
- Admin panel for broadcasting messages and managing orders

---

## 🛠️ Technologies Used

- **Python** (3.8+)
- **[python-telegram-bot](https://python-telegram-bot.org/ )** (v20+)
- **MySQL** for data storage
- **Telegram Bot API**

---

## 📦 Requirements

Before running the bot, ensure you have installed:

```bash
pip install python-telegram-bot --upgrade
pip install mysql-connector-python
```

and set telegram TOKEN in **config.py**

```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"