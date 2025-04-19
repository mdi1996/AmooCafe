from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import logging
import random
import os

TOKEN = '7532659685:AAFJytrCeABPZGxYQ7Ahf5DRx4sD0Q3mUKU'  # توکن ربات خودته
bot = Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# دستورات ربات
def start(update, context):
    update.message.reply_text(
        "سلام عموجون!\n\nمنوی کافه:\n- خوبی\n- چخبر\n- دلتنگم\n- دوستت دارم\n- خوابم میاد\n- عمو جون"
    )

def handle_message(update, context):
    text = update.message.text.strip().lower()

    if "سلام" in text:
        responses = [
            "سلام به روی ماهت عموجون",
            "سلام سلطان!! خوش اومدی",
            "سلام و صدتا سلام عمو🌹 جون 😍",
            "علیک سلام عمو جون، باد آمد و بوی عنبر آورد😁😍"
        ]
        update.message.reply_text(random.choice(responses))

    elif any(word in text for word in ['چخبر', 'چه خبر', 'چ خبر']):
        update.message.reply_text("خبرا که پیش شماست عموجون!")

    elif "کسی آنلاین نیست" in text:
        update.message.reply_text("من آنلاینم عموجون 😍 کاری داشتی؟")

    elif "عمو جون" in text:
        responses = [
            "جان دلم عمو؟ بگو ببینم چی شده!",
            "جانم عموجون؟ 😍 چیزی میل داری؟",
            "بفرمایید عموجون، یه قهوه گرم مخصوص شما☕️",
            "عموجون بفرما بشین، قهوه تازه و داغ با کیک تازه برات بیارم😁😍"
        ]
        update.message.reply_text(random.choice(responses))

    elif "اصل" in text and "اصلاح" not in text:
        update.message.reply_text("شما مامور ثبت احوالی؟ 😂😐")

    elif any(word in text for word in ['بیا پیوی', 'بیا پی وی']):
        update.message.reply_text("پیوی خطرناکه حسن😂🗿")

    elif any(word in text for word in ['خداحافظ', 'خدانگهدار', 'بای']):
        responses = [
            "خدانگهدار ستون😁🌹",
            "فعلا مواظب خودت باش سلطان ❤"
        ]
        update.message.reply_text(random.choice(responses))

    elif any(word in text for word in ['گشنمه', 'گرسنمه']):
        update.message.reply_text("چی میل داری عموجون؟ 😋")

    elif 'منوی کافه' in text or 'منو کافه' in text:
        keywords = [
            'سلام', 'چخبر', 'کسی آنلاین نیست', 'عمو جون', 'اصل', 'بیا پیوی', 'بیا پی وی',
            'خداحافظ', 'خدانگهدار', 'بای', 'گشنمه', 'گرسنمه', 'کافه لاته', 'موهیتو نعنایی',
            'کافه گلاسه', 'چای لاته', 'هات چاکلت', 'قهوه امریکانو', 'آیس کافی', 'اسموتی توت‌فرنگی',
            'چای ماسالا', 'لیموناد', 'فرپچینو', 'میلک‌شیک شکلاتی', 'چای سبز لاته', 'آیس تی',
            'اسموتی موز و بادام', 'قهوه ترک', 'چای ماته', 'شربت زعفران', 'آب پرتقال تازه', 'میلک‌شیک وانیلی'
        ]
        update.message.reply_text("کلمات کلیدی منوی کافه:\n- " + '\n- '.join(keywords))
        return

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

    for item in recipes:
        if item in text:
            update.message.reply_text(recipes[item])
            break

# وصل کردن فرمان‌ها
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# آدرس مخصوص دریافت پیام‌ها از تلگرام
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

# صفحه اصلی
@app.route('/')
def index():
    return 'ربات با موفقیت اجرا شد.'

# اجرا
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
