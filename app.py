import re
import os
import random
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = "7532659685:AAFJytrCeABPZGxYQ7Ahf5DRx4sD0Q3mUKU"
WEBHOOK_URL = "https://amoocafe.onrender.com/" + TOKEN

# --- کلمات کلیدی و پاسخ‌ها ---
keywords = {
    ("صبح بخیر", "صبحت بخیر", "صبح دل‌انگیز", "صبحت پر انرژی", "صبح شد", "صب بخیر"): [
        "صبحت بخیر رفیق کافه‌ای! وقتشه فنجان قهوه‌ت رو آماده کنم!",
        "صبح شد و کافه بازه! بیا یه فنجون آرامش بزنیم!",
    ],
    ("ظهر بخیر", "وقت ناهار", "ظهر شد", "نیم‌روز خوش", "ظهربخیر"): [
        "ظهر بخیر عزیزِ دلم! وقتشه یه قهوه سبک بزنیم وسط روز!",
        "ناهارتو خوردی؟ اگه نه بیا اینجا باهم ناهار بزنیم!",
    ],
    ("شب بخیر", "شب خوش", "شب شد", "شب قشنگی داشته باشی"): [
        "شب بخیر رفیق! بخواب تا خواب‌هات هم بوی قهوه بده!",
        "کافه فعلا بسته‌س ولی دلم همیشه به روت بازه عمو!",
    ],
    ("سلام", "سلااام", "درود", "هی", "های"): [
        "سلام سلطان! چطوری رفیق کافه‌ای من؟",
        "سلام! نور چشمای کافه اومد!",
    ],
    ("خوبی؟", "چطوری؟", "حالت چطوره؟", "چه خبر؟", "خوبی", "خبی", "چطوری", "حالت چطوره"): [
        "من خوبم، قهوه‌سازم سالمه، تو خوبی عموجون؟",
        "سلامتی تو عمو! قهوه تازه دم شده بیا قهوه بزنیم!",
    ],
    ("دلم گرفته", "حالم بده", "دلم تنگه", "افسرده‌م", "دلتنگی", "ناراحتم", "دلتنگم", "حوصله ندارم"): [
        "یه فنجون چای زعفرونی بزن، دلت وا شه رفیق!",
        "بیا حرف بزنیم، اینجا واسه دل دلتنگت بازه عمو جون!",
    ],
    ("پیوی", "پی وی", "pv", "private", "p v"): [
        "پیوی؟ اوه، نه دوست عزیز، پیوی برای قهوه‌های انحصاریه!",
        "پیوی؟! اینجا کافه‌ست، نه اتاق جلسات خصوصی!",
    ],
    ("اصل",): [
        "اسمش نازنین ممده، ۶۰ سالشه از یه وری!",
        "چیکار به اصلش داری؟ فیکه رو گردنش زده made in china!",
    ]
}

# --- کلمات و ایموجی‌های ری‌اکشن ---
reactions = {
    'سلام': '🫡',
    'عشق': '❤️',
    'دوست': '❤️',
    'رفیق': '❤️',
    'خوبی': '🥰',
    'چخبر': '🤔',
    'حبیبه': '🩵',
    'ماهان': '😎',
    'ایلار': '💜',
    'آیدا': '🧡',
    'ساحل': '💛',
    'عمو': '☕',
    'ابول': '😁',
}

# --- نرمال‌سازی متن ---
def normalize_text(text):
    text = re.sub(r'[؟?!]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('‌', ' ')
    text = text.replace('آ', 'ا')
    return text.strip().lower()

# --- پیدا کردن پاسخ ---
def get_response(text):
    processed = normalize_text(text)

    if processed == "/start":
        return (
            "من عمو کافه‌چی هستم!\n"
            "سازنده: Mehdi_mashih\n"
            "برای دیدن لیست کلمات، بفرست: منوی کلمات"
        )

    if processed == "منوی کلمات":
        return "\n".join(["- " + list(group)[0] for group in keywords.keys()])

    if processed == "سازنده":
        return "Mehdi_mashih"

    for key_group, responses in keywords.items():
        for keyword in key_group:
            if keyword in processed:
                return random.choice(responses)

    return None

# --- مدیریت پیام‌ها ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message:
        text = message.text
        chat_id = message.chat_id
        message_id = message.message_id

        # ری‌اکشن اگر شامل کلمه‌ای بود
        for word, emoji in reactions.items():
            if word in text:
                try:
                    await message.react(emoji)
                    break
                except Exception as e:
                    print(f"خطا در ری‌اکت: {e}")

        # پاسخ به کلمات کلیدی
        response = get_response(text)
        if response:
            await context.bot.send_message(chat_id=chat_id, text=response, reply_to_message_id=message_id)

# --- مدیریت خطاها ---
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Error: {context.error}")

# --- ساخت اپ Flask ---
app = Flask(__name__)

@app.route("/")
def home():
    return "کافه آماده‌ست!"

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(await request.get_json(force=True), context.application.bot)
    await context.application.process_update(update)
    return "ok"

# --- ران کردن اپلیکیشن ---
if __name__ == "__main__":
    from telegram.ext import ApplicationBuilder

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.add_error_handler(error_handler)

    # ست کردن وبهوک
    import asyncio
    async def main():
        await application.bot.set_webhook(WEBHOOK_URL)
        app.run(host="0.0.0.0", port=5000)

    asyncio.run(main())
