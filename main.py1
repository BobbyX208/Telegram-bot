import os
import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from flask import Flask
from threading import Thread

# Flask Web Server to keep the bot alive
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Load sensitive data from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # Example: "@modapps27"

# OpenAI API Configuration
openai.api_key = OPENAI_API_KEY

# Bot Command Handlers
def start(update, context):
    update.message.reply_text(
        "Yo! I'm RealbobBot here to assist you! ⭐",
        reply_markup=ReplyKeyboardMarkup(
            [["/help", "/ai_chat"], ["/forward", "/stats"]],
            resize_keyboard=True
        )
    )

def help_command(update, context):
    update.message.reply_text(
        "Commands you can use:\n"
        "/start - Start the bot\n"
        "/help - Get a list of commands\n"
        "/ai_chat - Chat with AI\n"
        "/forward - Forward files to the channel\n"
        "/stats - Show channel stats"
    )

def ai_chat(update, context):
    user_message = " ".join(context.args)
    if not user_message:
        update.message.reply_text("Please enter a message after /ai_chat.")
        return

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        ai_reply = response.choices[0].message["content"]
        update.message.reply_text(ai_reply)
    except Exception as e:
        update.message.reply_text("Sorry, I couldn't fetch an AI response. Try again later.")

def forward_file(update, context):
    if update.message.document:
        update.message.bot.send_document(CHANNEL_ID, document=update.message.document.file_id)
        update.message.reply_text("File forwarded successfully!")
    elif update.message.photo:
        update.message.bot.send_photo(CHANNEL_ID, photo=update.message.photo[-1].file_id)
        update.message.reply_text("Photo forwarded successfully!")
    elif update.message.video:
        update.message.bot.send_video(CHANNEL_ID, video=update.message.video.file_id)
        update.message.reply_text("Video forwarded successfully!")
    else:
        update.message.reply_text("Send a document, photo, or video to forward.")

def stats(update, context):
    update.message.reply_text("Stats tracking will be implemented soon!")

# Main Function
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("ai_chat", ai_chat))
    dp.add_handler(MessageHandler(Filters.document | Filters.photo | Filters.video, forward_file))
    dp.add_handler(CommandHandler("stats", stats))

    # Start Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    keep_alive()  # Keep the bot alive with Flask
    main()
