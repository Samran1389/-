import os
import requests
import telebot
from dotenv import load_dotenv

# 🛠 خواندن متغیرهای محیطی (در تست لوکال)
load_dotenv()

# 📌 دریافت مقادیر از متغیرهای محیطی
BOT_TOKEN = os.getenv("7939908094:AAE38bx1UUSju18qJKmFlYszMFaR41hjNh8")
API_KEY = os.getenv("67c230a24185c")

# 🤖 راه‌اندازی ربات تلگرام
bot = telebot.TeleBot(BOT_TOKEN)

# 🎯 تابع دانلود از اینستاگرام
def download_instagram_media(instagram_url):
    api_url = "https://api.example.com/instagram/download"
    params = {
        'api_key': API_KEY,
        'url': instagram_url
    }
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get("download_url")  # 📥 لینک دانلود
    else:
        return None

# 📌 دستور `/start`
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 سلام! لینک اینستاگرام را بفرست تا دانلود کنم. \n\n📌 مثال: /download https://www.instagram.com/reel/xxxxx")

# 📌 دستور `/download <url>`
@bot.message_handler(commands=['download'])
def download_handler(message):
    try:
        instagram_url = message.text.split(" ")[1]  # دریافت لینک اینستاگرام
        download_link = download_instagram_media(instagram_url)

        if download_link:
            bot.send_message(message.chat.id, f"✅ لینک دانلود:\n{download_link}")
        else:
            bot.send_message(message.chat.id, "❌ دانلود ممکن نیست. لینک را بررسی کنید.")
    except IndexError:
        bot.send_message(message.chat.id, "❌ لطفاً لینک اینستاگرام را ارسال کنید.\n\n📌 مثال: /download https://www.instagram.com/reel/xxxxx")

# 🔄 اجرای ربات
bot.polling()