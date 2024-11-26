import openai  # For AI responses
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread
import os

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

# Load Secrets
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Add this in Secrets
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Add this in Secrets

openai.api_key = OPENAI_API_KEY

# Bot Commands
def start(update, context):
    update.message.reply_text("Yo! I'm RealbobBot, here to manage the channel! ⭐")

def help_command(update, context):
    update.message.reply_text(
        "Here are the commands:\n"
        "/start - Welcome message\n"
        "/help - List of commands\n"
        "/schedule - Schedule posts\n"
        "/stats - Show channel stats\n"
        "/poll - Create a poll\n"
        "/rules - Display rules\n"
    )

def chatgpt_response(update, context):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        ai_reply = response["choices"][0]["message"]["content"]
        update.message.reply_text(ai_reply)
    except Exception as e:
        update.message.reply_text("Sorry, I can't respond right now!")

# File Forwarding without Forwarded Tag
def forward_to_channel(update, context):
    channel_id = "CHANNEL_ID_HERE"  # Replace with your actual channel's username
    if update.message.document:
        file = update.message.document.get_file()
        file.download('temp_file')
        context.bot.send_document(chat_id=channel_id, document=open('temp_file', 'rb'))
        update.message.reply_text(f"File '{update.message.document.file_name}' forwarded!")
    elif update.message.photo:
        photo = update.message.photo[-1].get_file()
        photo.download('temp_photo.jpg')
        context.bot.send_photo(chat_id=channel_id, photo=open('temp_photo.jpg', 'rb'))
        update.message.reply_text("Photo forwarded!")
    elif update.message.video:
        video = update.message.video.get_file()
        video.download('temp_video.mp4')
        context.bot.send_video(chat_id=channel_id, video=open('temp_video.mp4', 'rb'))
        update.message.reply_text("Video forwarded!")
    else:
        update.message.reply_text("Send a document, photo, or video to forward.")

# Button Menu Example
def button_menu(update, context):
    buttons = [
        [InlineKeyboardButton("ChatGPT", callback_data='chatgpt')],
        [InlineKeyboardButton("Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text("Choose an option:", reply_markup=reply_markup)

def button_handler(update, context):
    query = update.callback_query
    if query.data == 'chatgpt':
        query.message.reply_text("Type a message for ChatGPT!")
    elif query.data == 'help':
        query.message.reply_text("This bot helps you manage your channel with cool features.")

# Main Function
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("menu", button_menu))
    dp.add_handler(MessageHandler(Filters.document | Filters.photo | Filters.video, forward_to_channel))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chatgpt_response))

    # Callback Query Handler
    dp.add_handler(telegram.ext.CallbackQueryHandler(button_handler))

    # Start Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    keep_alive()
    main()
