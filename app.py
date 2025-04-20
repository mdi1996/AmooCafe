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

# کلمات کلیدی و پاسخ‌ها
keywords = {
    "صبح بخیر صبح دل انگیز صبحت پر انرژی صبح شد صب بخیر صبحت بخیر": [
        "صبحت بخیر رفیق کافه‌ای! وقتشه فنجان قهوه‌ت رو آماده کنم!"
    ],
    "ظهر بخیر وقت ناهار ظهر شد نیم‌روز خوش ظهربخیر": [
        "ظهر بخیر! یه نوشیدنی خنک می‌چسبه؟"
    ],
    "شب بخیر شب خوش شب شد شب قشنگی داشته باشی": [
        "شب خوش دوست کافه‌ای من! خوابای شیرین ببینی."
    ],
    "سلام سلااام درود هی های": [
        "سلام به روی ماهت!"
    ],
    "خوبی؟ چطوری؟ حالت چطوره؟ چه خبر؟ خوبی خبی چطوری حالت چطوره": [
        "من خوبم که تو اومدی! تو خوبی؟"
    ],
    "دلم گرفته حالم بده دلم تنگه افسرده‌م دلتنگی ناراحتم دلتنگم. حوصله ندارم": [
        "یه لیوان قهوه با دل آرام برات می‌ریزم..."
    ],
    "بیکارم حوصلم سر رفته چیکار کنم؟ بیکاری بی کاری بی حوصله م بی حوصلگی": [
        "بیایید یه نوشیدنی پیشنهاد بدم!"
    ],
    "گرسنگی تشنگی گشنمه گرسنمه تشنمه": [
        "بیا منوی نوشیدنی رو ببین، چیزی پیدا میشه!"
    ],
    "عمو عمو جون عموجون کافه‌چی عمو!": [
        "خودم‌ام! چی می‌خوری؟"
    ],
    "خداحافظ فعلا بای می‌رم خدا حافظ خدانگهدار خدا نگه دار بای بای رفتم میرم": [
        "خدانگهدار رفیق! زود برگرد."
    ],
    "لطیفه جوک بخندونم یه چیزی بگو بخندیم جک": [
        "یه نفر رفت کافی‌شاپ گفت یه چیزی بده بخندم، گارسون گفت: قهوه‌مون تلخه!"
    ],
    "تنها کسی نیست؟ حوصله ندارم تنهایی کسی نیست کسی نیس کسی انلاین نیس؟ کسی انلاین نیس کسی آنلاین نیست؟ کسی آنلاین نیست کسی هست کسی هست؟ کسی انلاین هست؟ کسی آنلاین هس؟": [
        "من اینجام! همیشه هستم."
    ],
    "دوستت دارم عاشقت شدم دل دادم عشق": [
        "منم دوستت دارم رفیق بااحساس من!"
    ],
    "پیوی": [
        "بیا تو پی‌وی، حرفای قشنگ بزنیم!"
    ],
    "اصل": [
        "تو خود اصل محبتی رفیق!"
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

    if processed in ["/start", "استارت", "معرفی"]:
        return (
            "سلام من عمو کافه چی ام من یک ربات چت محور تلگرامی هستم که توسط عمو ساخته شدم لطفاً هرگونه انتقاد و پیشنهاد خودتونو به اون بگید\n\n"
            "ارادتمند شما عمو❤\n\n"
            "منوی کلمات \n"
            "منوی نوشیدنی \n"
            "سازنده       Mehdi_mashih"
        )

    if processed == "منوی نوشیدنی":
        return "\n".join([f"- {drink}" for drink in beverages.keys()])

    if processed == "منوی کلمات":
        return "\n".join([f"- {kw}" for kw in keywords.keys()])

    if processed == "سازنده":
        return "Mehdi_mashih"

    if re.search(r'\bاصل\b', processed):
        return random.choice(keywords["اصل"])

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

    print("پیام کاربر:", text)
    print("پاسخ ربات:", response)

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
