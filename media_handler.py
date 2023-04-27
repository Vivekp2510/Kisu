# media_handler.py
# media_handler.py

import json
import os
from telegram import InputFile, Update
from telegram.ext import CallbackContext, CommandHandler

# Other imports ...

SHARED_MEDIA_FILE = "shared_media.json"


def load_shared_media():
    if not os.path.exists(SHARED_MEDIA_FILE):
        return []
    with open(SHARED_MEDIA_FILE, "r") as f:
        return json.load(f)


def save_shared_media():
    with open(SHARED_MEDIA_FILE, "w") as f:
        json.dump(shared_media, f)


shared_media = load_shared_media()


# Other functions ...

def add_media(update: Update, context: CallbackContext) -> None:
    message = update.message
    user_id = message.from_user.id

    # Replace YOUR_TELEGRAM_USER_ID with your actual Telegram user ID
    if user_id != 634312042:
        return

    if message.reply_to_message:
        media_message = message.reply_to_message
        chat_id = media_message.chat_id

        if media_message.photo:
            shared_media.append(("photo", media_message.photo[-1].file_id, chat_id))
        elif media_message.video:
            shared_media.append(("video", media_message.video.file_id, chat_id))
        elif media_message.animation:
            shared_media.append(("animation", media_message.animation.file_id, chat_id))

        save_shared_media()
        message.reply_text("Media file added to the bot's storage.")
    else:
        message.reply_text("Please reply to a media message with /addmedia to add it to the bot's storage.")


def store_media(update: Update, context: CallbackContext) -> None:
    # ... same as before ...

    save_shared_media()


# Other functions ...

def main(dp=None) -> None:
    # ... same as before ...

    dp.add_handler(CommandHandler('addmedia', add_media))
    # ... other handlers ...

    # ... same as before ...
