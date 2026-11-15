import telebot
import random
import time
import threading
from faker import Faker
from flask import Flask
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

bot = telebot.TeleBot(BOT_TOKEN)
fake = Faker('ar_EG')
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def generate_fake_number():
    return f"+20 1{random.randint(0,2)}{random.randint(10000000, 99999999)}"

def daily_sender():
    while True:
        number = generate_fake_number()
        try:
            bot.send_message(CHAT_ID, f"رقم النهاردة الفيك للتجربة:\n{number}\n\nللتجربة والبرمجة فقط")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(86400)

@bot.message_handler(commands=['start', 'number'])
def send_now(message):
    number = generate_fake_number()
    bot.reply_to(message, f"رقم فيك حالاً:\n{number}")

def run_bot():
    threading.Thread(target=daily_sender, daemon=True).start()
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
