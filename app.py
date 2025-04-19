from flask import Flask, request
from telegram import Bot, Update, Message
from telegram.ext import CommandHandler, MessageHandler, Filters, Dispatcher, Updater
import logging
import random
import os

# توکن ربات
TOKEN = '7532659685:AAFJytrCeABPZGxYQ7Ahf5DRx4sD0Q3mUKU'

app = Flask(__name__)
bot = Bot(token=TOKEN)

# تنظیمات لاگ‌گیری
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# تابع /start
def start(update, context):
    items = [
        "سلام", "چخبر", "کسی آنلاین نیست", "عمو جون", "خداحافظ",
        "گشنمه", "منوی کافه", "اصل", "بیا پیوی", "بیا پی وی",
        'کافه لاته', 'موهیتو نعنایی', 'کافه گلاسه', 'چای لاته', 'هات چاکلت',
        'قهوه امریکانو', 'آیس کافی', 'اسموتی توت‌فرنگی', 'چای ماسالا',
        'لیموناد', 'فرپچینو', 'میلک‌شیک شکلاتی', 'چای سبز لاته', 'آیس تی',
        'اسموتی موز و بادام', 'قهوه ترک', 'چای ماته', 'شربت زعفران',
        'آب پرتقال تازه', 'میلک‌شیک وانیلی'
    ]
    list_text = "کلیدواژه‌ها و نوشیدنی‌های کافه:\n" + "\n".join(f"- {item}" for item in items)
    update.message.reply_text(list_text)

# دیکشنری نوشیدنی‌ها و طرز تهیه‌شون
recipes = {
    'کافه لاته': 'اسپرسو را با شیر گرم مخلوط کنید و روی آن فوم شیر بریزید.',
    'موهیتو نعنایی': 'نعناع تازه، لیمو، شکر و آب گازدار را ترکیب کنید.',
    'کافه گلاسه': 'قهوه سرد، بستنی و شیر را مخلوط کنید و با سس شکلات تزئین کنید.',
    'چای لاته': 'چای سیاه را با شیر گرم و دارچین ترکیب کنید.',
    'هات چاکلت': 'شیر گرم را با پودر کاکائو و شکلات تخته‌ای مخلوط کنید.',
    'قهوه امریکانو': 'اسپرسو را با آب داغ رقیق کنید.',
    'آیس کافی': 'قهوه سرد را با یخ و شیر مخلوط کنید.',
    'اسموتی توت‌فرنگی': 'توت‌فرنگی، شیر و یخ را در مخلوط‌کن ترکیب کنید.',
    'چای ماسالا': 'چای سیاه را با شیر و ادویه‌های ماسالا دم کنید.',
    'لیموناد': 'آب لیمو، شکر و آب سرد را مخلوط کنید.',
    'فرپچینو': 'قهوه سرد، شیر، یخ و شکر را در مخلوط‌کن ترکیب کنید.',
    'میلک‌شیک شکلاتی': 'بستنی شکلاتی، شیر و شکلات تخته‌ای را مخلوط کنید.',
    'چای سبز لاته': 'چای سبز را با شیر گرم مخلوط کنید.',
    'آیس تی': 'چای سرد را با یخ و لیمو سرو کنید.',
    'اسموتی موز و بادام': 'موز، شیر بادام و یخ را ترکیب کنید.',
    'قهوه ترک': 'قهوه ترک را با آب و شکر دم کنید.',
    'چای ماته': 'چای ماته را با آب داغ دم کنید و با نی سرو کنید.',
    'شربت زعفران': 'زعفران، شکر و آب را مخلوط کنید.',
    'آب پرتقال تازه': 'پرتقال را آبگیری کنید و سرو کنید.',
    'میلک‌شیک وانیلی': 'بستنی وانیلی و شیر را مخلوط کنید.'
}

# تابع پاسخ‌دهی به پیام‌ها
def handle_message(update, context):
    message: Message = update.message
    text = message.text.strip().lower()

    if "اصل" in text.split():
        message.reply_text("شما مامور ثبت احوالی؟ 😂😐")
        return

    if any(phrase in text for phrase in ["بیا پیوی", "بیا پی وی"]):
        message.reply_text("پیوی خطرناکه حسن😂🗿")
        return

    if message.reply_to_message:
        return

    if "سلام" in text:
        responses = [
            "سلام به روی ماهت عموجون",
            "سلام سلطان!! خوش اومدی",
            "سلام و صدتا سلام عمو🌹 جون 😍",
            "علیک سلام عمو جون، باد آمد و بوی عنبر آورد😁😍"
        ]
        message.reply_text(random.choice(responses))
    elif any(w in text for w in ["چخبر", "چه خبر", "چ خبر"]):
        message.reply_text("خبرا که پیش شماست عموجون!")
    elif "کسی آنلاین نیست" in text:
        message.reply_text("من آنلاینم عموجون 😍 کاری داشتی؟")
    elif "عمو جون" in text:
        responses = [
            "جان دلم عمو؟ بگو ببینم چی شده!",
            "جانم عموجون؟ 😍 چیزی میل داری؟",
            "بفرمایید عموجون، یه قهوه گرم مخصوص شما☕️",
            "عموجون بفرما بشین، قهوه تازه و داغ با کیک تازه برات بیارم😁😍"
        ]
        message.reply_text(random.choice(responses))
    elif any(w in text for w in ["خداحافظ", "خدانگهدار", "بای"]):
        responses = [
            "خدانگهدار ستون😁🌹",
            "فعلا مواظب خودت باش سلطان ❤"
        ]
        message.reply_text(random.choice(responses))
    elif any(w in text for w in ["گشنمه", "گرسنمه"]):
        message.reply_text("چی میل داری عموجون؟ 😋")
    elif 'منوی کافه' in text or 'منو کافه' in text:
        message.reply_text("بگو ببینم چی می‌خوای تا طرز تهیه‌شو بگم عموجون!")
    else:
        for item, recipe in recipes.items():
            if item in text:
                message.reply_text(recipe)
                break

# راه‌اندازی دیسپچر و هندلرها
updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# روت‌های فلَسک
@app.route('/' + TOKEN, methods=['POST'])
def respond():
    update = Update.de_json(request.get_json(force=True), bot)
    dp.process_update(update)
    return 'ok'

@app.route('/')
def index():
    return 'ربات با موفقیت اجرا شد.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
