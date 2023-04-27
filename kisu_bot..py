import logging
import random
from datetime import datetime, timedelta
from telegram import Update, InputMediaPhoto, InputMediaVideo
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
# main.py

from media_handler import add_media, store_media, shared_media

# ... rest of the code ...

# Enable logging
logging.basicConfig(level=logging.INFO)

# Replace your token here
API_TOKEN = '6188645344:AAEuGHchVjegDa2sc-7h1qeHrGxprIXmE58'

# Store media files sent by users
shared_media = []

# Store the timestamp of the last /kisu command for each user and chat
last_kisu_call = {}

# Random text pool
text_pool = [
    "Kisu I want to Kiss U",
    "Kisu sends his ashirwad",
    "Short kings rejoice!",
    "Yo it’s Chief Kish!",
    "Call me daddy kish",
    "I am recruiting for al-qaeda pls send me ur resume/linkedIn",
    "No face no case",
    "Why do puja to maharaj when you can do it to Kisu",
    "Kisu de Akbar",
    "Malraja",
    "Ajaybha’s very own Mal-man",
    "Akshar Baby u smell",
    "KisuBisu",
    "Harsh I love u",
    "What’s the weather Ajajbhai?"
]

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! I am Kisu bot.')

def kisu(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    now = datetime.utcnow()

    # Cooldown timer (in seconds)
    cooldown = 5

    user_chat_key = (user_id, chat_id)
    if user_chat_key in last_kisu_call and now - last_kisu_call[user_chat_key] < timedelta(seconds=cooldown):
        remaining_time = int(cooldown - (now - last_kisu_call[user_chat_key]).total_seconds())
        update.message.reply_text(f"Please wait {remaining_time} seconds before calling /kisu again.")
        return

    last_kisu_call[user_chat_key] = now

    chat_media = [media for media in shared_media if media[2] == chat_id]

    if not chat_media:
        update.message.reply_text("No media files have been shared in this group chat yet.")
        return

    update.message.reply_text("🙏 #KisuDailyDarshan #Kisu\n\n_" + random.choice(text_pool) + "_", parse_mode="Markdown")

    random_media = random.choice(chat_media)
    media_type, file_id = random_media[0], random_media[1]

    if media_type == "photo":
        update.message.reply_photo(photo=file_id)
    elif media_type == "video":
        update.message.reply_video(video=file_id)
    elif media_type == "animation":
        update.message.reply_animation(animation=file_id)

def store_media(update: Update, context: CallbackContext) -> None:
    message = update.message
    chat_id = message.chat_id

    if message.photo:
        shared_media.append(("photo", message.photo[-1].file_id, chat_id))
    elif message.video:
        shared_media.append(("video", message.video.file_id, chat_id))
    elif message.animation:
        shared_media.append(("animation", message.animation.file_id, chat_id))

def main() -> None:
    updater = Updater(API_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command and message handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('kisu', kisu))
    dp.add_handler(MessageHandler((~Filters.command) & (Filters.photo | Filters.video | Filters.animation), store_media))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
