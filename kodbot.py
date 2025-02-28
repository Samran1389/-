import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import instaloader
import re

# 🎯 توکن ربات را اینجا قرار بده
TOKEN = "7939908094:AAE38bx1UUSju18qJKmFlYszMFaR41hjNh8"
bot = telebot.TeleBot(TOKEN)

# 📥 ایجاد نمونه Instaloader برای دانلود از اینستاگرام
loader = instaloader.Instaloader()

# 🎨 ایجاد کیبورد دکمه‌ای
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("📥 دانلود پست اینستاگرام")
    btn2 = KeyboardButton("ℹ️ راهنما")
    markup.add(btn1, btn2)
    return markup

# 🏠 پیام خوش‌آمدگویی
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, 
        "👋 سلام! به ربات دانلود اینستاگرام خوش آمدی.\n\n🔹 لینک پست اینستاگرام را ارسال کن تا آن را دانلود کنم.",
        reply_markup=main_menu()
    )

# 📥 دانلود پست اینستاگرام
@bot.message_handler(func=lambda message: message.text == "📥 دانلود پست اینستاگرام")
def ask_for_url(message):
    bot.send_message(message.chat.id, "🔗 لطفا لینک پست اینستاگرام را ارسال کنید.")

@bot.message_handler(func=lambda message: "instagram.com" in message.text)
def download_instagram_post(message):
    url = message.text
    try:
        # 🛠 استخراج کد پست از لینک
        short_code = re.search(r"instagram\.com/p/([A-Za-z0-9_-]+)/?", url).group(1)
        
        # 🎬 دریافت اطلاعات پست
        post = instaloader.Post.from_shortcode(loader.context, short_code)

        # 📤 ارسال تصویر یا ویدیو
        media_url = post.video_url if post.is_video else post.url
        bot.send_message(message.chat.id, "⏳ در حال دانلود...")
        
        if post.is_video:
            bot.send_video(message.chat.id, media_url)
        else:
            bot.send_photo(message.chat.id, media_url)

    except Exception as e:
        bot.reply_to(message, f"❌ خطایی رخ داد: {str(e)}")

# ℹ️ راهنمای استفاده
@bot.message_handler(func=lambda message: message.text == "ℹ️ راهنما")
def send_help(message):
    bot.send_message(
        message.chat.id, 
        "📌 **راهنمای استفاده:**\n"
        "1️⃣ لینک یک پست اینستاگرام را ارسال کن.\n"
        "2️⃣ منتظر بمان تا دانلود انجام شود.\n"
        "3️⃣ فایل برای شما ارسال خواهد شد.\n\n"
        "🔹 **توجه:** فقط پست‌های عمومی قابل دانلود هستند!",
        parse_mode="Markdown"
    )

# 🎯 اجرای ربات
bot.polling()