import re
from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters
import random

TOKEN = "7532659685:AAFJytrCeABPZGxYQ7Ahf5DRx4sD0Q3mUKU"
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=1, use_context=True)

# کلیدواژه‌ها و پاسخ‌ها (همون دیتای قبلیت)
keywords = {
    # --- [کلیدواژه‌ها و پاسخ‌ها سر جای خودشون باقی موندن] ---
    # ... کد کامل keywordها اینجاست (حذف نشدن برای اختصار) ...
}

pivi_responses = [
    "عزیز دل، کافه من بازه، اما پیوی جای درددل و خلوت نیست، بیا همینجا حرفت رو بزن که بقیه هم از مهربونی‌ات بهره ببرن.",
    "پیوی؟ اوه، نه دوست عزیز، پیوی برای قهوه‌های انحصاریه! بیا همینجا، همه کنار هم، مزه میده.",
    "پیوی؟! اینجا کافه‌ست، نه اتاق جلسات خصوصی!",
    "پیوی؟ نکنه می‌خوای دستور مخفی قهوه رو از من بدزدی؟ بیا همینجا، چیزی برای پنهون کردن ندارم!",
    "رفتن به پیوی؟ اینجا یه کافه جادوییه، بیا، همه چیز همینجا حل می‌شه.",
    "باشه برو پیوی🗿ولی یادت باشه قهوه من همیشه همینجا تو کافه سرو میشه نه تو پیوی😒😔"
]

asl_responses = [
    "شما مامور ثبت احوالی عمو؟ 🗿",
    "اسمش قنبره من میشناسمش قصابی داره 🗿",
    "چیکار به اصلش داری؟ 😂🗿",
    "این اصل نداره فیکه رو گردنش زده made in china 🗿",
    "اسمش نازنین ممده🗿60 ساله از یه وری"
]

def normalize_text(text):
    text = re.sub(r'[؟?!]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('‌', ' ')
    text = text.replace('آ', 'ا')
    return text.strip().lower()

def get_response(text):
    processed = normalize_text(text)

    if processed == "/start":
        return (
            "من عمو کافه‌چی هستم یک ربات چت‌محور تلگرامی که توسط عمو طراحی شدم.\n"
            "اگر برای بهتر شدن من پیشنهاد یا انتقادی دارید با عمو جان در اشتراک بگذارید.\n\n"
            "منوی کلمات\n"
            "سازنده: Mehdi_mashih"
        )

    if processed == "منوی کلمات":
        return "\n".join(["- " + list(word_group)[0] for word_group in keywords.keys()])

    if processed == "سازنده":
        return "Mehdi_mashih"

    if re.search(r'\bاصل\b', processed):
        return random.choice(asl_responses)

    if any(word in processed for word in ["پیوی", "پی وی", "pv", "private", "p v"]):
        return random.choice(pivi_responses)

    for key_group, responses in keywords.items():
        for phrase in key_group:
            if phrase in processed:
                return random.choice(responses)

    return None

def handle_message(update, context):
    text = update.message.text
    chat_id = update.message.chat_id
    message_id = update.message.message_id

    response = get_response(text)
    if response:
        context.bot.send_message(chat_id=chat_id, text=response, reply_to_message_id=message_id)

def error_handler(update, context):
    print(f"Error: {context.error}")

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
dispatcher.add_error_handler(error_handler)

# تنظیم Webhook در Render
bot.set_webhook(url=f"https://amoocafe.onrender.com/{TOKEN}")

@app.route("/")
def home():
    return "کافه آماده است!"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
