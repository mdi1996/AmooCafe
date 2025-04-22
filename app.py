import re
from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters
import random
from queue import Queue

TOKEN = "7532659685:AAFJytrCeABPZGxYQ7Ahf5DRx4sD0Q3mUKU"
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)
update_queue = Queue()
dispatcher = Dispatcher(bot, update_queue, workers=4, use_context=True, run_async=True)

# (کلیدواژه‌ها و لیست‌هایت رو همون‌طور نگه‌دار، تغییری لازم نیست...)

# تابع نرمال‌سازی و get_response بدون تغییر:
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

# تابع اصلاح‌شده‌ی handle_message برای ریپلای:
def handle_message(update, context):
    text = update.message.text
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    response = get_response(text)
    if response:
        context.bot.send_message(chat_id=chat_id, text=response, reply_to_message_id=message_id)

# اضافه کردن handler و error handler
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

def error_handler(update, context):
    print(f"Error: {context.error}")

dispatcher.add_error_handler(error_handler)

# Webhook route
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
