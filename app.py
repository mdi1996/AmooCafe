import re
from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters
import random

TOKEN = "7532659685:AAFJytrCeABPZGxYQ7Ahf5DRx4sD0Q3mUKU"
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=1, use_context=True)

# دیتای نوشیدنی‌ها
beverages = {
    "اسپرسو": "برای تهیه اسپرسو، به میزان ۲۳ گرم پودر قهوه تازه آسیاب‌شده نیاز دارید...",
    "کاپوچینو": "برای تهیه کاپوچینو ابتدا اسپرسو رو تهیه کنید و سپس شیر را بخار دهید...",
    "لاته": "تهیه لاته مشابه کاپوچینو است، اما شیر بیشتری نسبت به کف شیر استفاده می‌شود...",
    "شیک شکلاتی": "شکلات ذوب‌شده و شیر سرد را با هم مخلوط کنید...",
    "چای زعفرونی": "چای سیاه را به همراه زعفران دم کرده و با کمی شکر سرو کنید.",
    "شیک وانیلی": "شیر، شکر و پودر وانیل را با هم مخلوط کرده و در مخلوط‌کن بزنید.",
    "قهوه ترک": "پودر قهوه ترک را با آب مخلوط کرده و روی حرارت ملایم بجوشانید."
}

# کلیدواژه‌ها و پاسخ‌ها
keywords = {
    "صبح بخیر صبح دل انگیز صبحت پر انرژی صبح شد صب بخیر صبحت بخیر": [
        "صبحت بخیر رفیق کافه‌ای! وقتشه فنجان قهوه‌ت رو آماده کنم! ☀️☕",
        "صبح شد و کافه بازه! بیا یه فنجون آرامش بزنیم! 🌅🍯",
        "بیدار شدی؟ یعنی وقتشه برات قهوه بریزم و موزیک پخش کنم! 🎶☕",
        "صبحت خوش! بخوای یا نخوای امروز خیلی قشنگه عمو چون تو هستی! ✨🌞",
        "سلام به خورشیدِ خودم! قهوه داغ با یه لبخند آماده‌ست! ☕️😊"
    ],
    "لطیفه جوک بخندونم یه چیزی بگو بخندیم جک": [
        "یه قهوه با شیر ازدواج کرد، بچه‌ش شد کاپوچینو! ☕👶",
        "یه اسپرسو رفت خواستگاری، گفتن خیلی تلخی! 🥲💔"
    ],
    "پیوی": [
        "پیوی؟ اوه، نه دوست عزیز، پیوی برای قهوه‌های انحصاریه! بیا همینجا، همه کنار هم، مزه میده.",
        "عزیز دل، کافه من بازه، اما پیوی جای درددل و خلوت نیست، بیا همینجا حرفت رو بزن که بقیه هم از مهربونی‌ات بهره ببرن.",
        "پیوی؟! اینجا کافه‌ست، نه اتاق جلسات خصوصی!",
        "پیوی؟ نکنه می‌خوای دستور مخفی قهوه رو از من بدزدی؟ بیا همینجا، چیزی برای پنهون کردن ندارم!",
        "رفتن به پیوی؟ اینجا یه کافه جادوییه، بیا، همه چیز همینجا حل می‌شه.",
        "باشه برو پیوی🗿ولی یادت باشه قهوه من همیشه همینجا تو کافه سرو میشه نه تو پیوی😒😔"
    ],
    "اصل": [
        "شما مامور ثبت احوالی عمو؟ 🗿",
        "اسمش قنبره من میشناسمش قصابی داره 🗿",
        "چیکار به اصلش داری؟ 😂🗿",
        "این اصل نداره فیکه رو گردنش زده made in china 🗿",
        "اسمش نازنین ممده🗿60 ساله از یه وری"
    ]
}

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
            "سلام من عمو کافه‌چی هستم می‌تونید منو «عمو» صدا کنید.\n"
            "من یک ربات چت‌محور تلگرامی‌ام که برای گرم کردن حال و هوای گروه ساخته شدم!\n"
            "پیشنهاد یا انتقادی داشتی به سازنده پیام بده\n\n"
            "منوی نوشیدنی\n"
            "منوی کلمات"
        )

    if processed == "منوی نوشیدنی":
        return "\n".join([f"- {drink}" for drink in beverages.keys()])

    if processed == "منوی کلمات":
        return "\n".join([
            "- پیوی",
            "- اصل"
        ])

    if processed == "سازنده":
        return "Mehdi_mashih"

    # بررسی دقیق فقط کلمه "اصل"
    if re.search(r'\bاصل\b', processed):
        return random.choice(keywords["اصل"])

    # بررسی کلمات مربوط به پیوی
    pivi_keywords = ["پیوی", "پی وی", "pv", "private", "p v"]
    if any(p in processed for p in pivi_keywords):
        return random.choice(keywords["پیوی"])

    for drink_name in beverages:
        if processed == normalize_text(drink_name):
            return beverages[drink_name]

    for key_group, responses in keywords.items():
        if any(word in processed for word in key_group.split()):
            return random.choice(responses)

    return None

def handle_message(update, context):
    text = update.message.text
    chat_id = update.message.chat_id
    response = get_response(text)
    if response:
        context.bot.send_message(chat_id=chat_id, text=response)

def error_handler(update, context):
    print(f"Error: {context.error}")

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
dispatcher.add_error_handler(error_handler)

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
