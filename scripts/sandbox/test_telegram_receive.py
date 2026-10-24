import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Load environment variables from .env file
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start_command(update, context):
    user = update.effective_user
    chat_id = update.effective_chat.id
    logger.info("Received /start from user %s (Chat ID: %s)", user.username or user.first_name, chat_id)
    await update.message.reply_text(
        f"Hello {user.first_name}! Telegram receiver test bot is running.\n"
        f"Your Chat ID: {chat_id}"
    )


async def ping_command(update, context):
    await update.message.reply_text("pong! Connection is working.")


async def handle_text_message(update, context):
    user = update.effective_user
    chat_id = update.effective_chat.id
    text = update.message.text
    sender_name = user.username or user.first_name

    logger.info("[New Message] Chat ID: %s | From: %s | Text: %s", chat_id, sender_name, text)
    print(f"\n--- INCOMING TELEGRAM MESSAGE ---")
    print(f"From: {sender_name} (ID: {user.id})")
    print(f"Chat ID: {chat_id}")
    print(f"Message: {text}")
    print(f"---------------------------------\n")

    # Echo receipt back to sender
    await update.message.reply_text(f"Echo: {text}")


def main():
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your_telegram_bot_token_here":
        print("\n[ERROR] TELEGRAM_BOT_TOKEN is missing or not configured.")
        print("Please set your bot token in the root '.env' file:")
        print("TELEGRAM_BOT_TOKEN=\"123456789:ABCdefGHIjklMNOpqrsTUVwxyz\"\n")
        return

    print("Initializing Telegram bot listener...")
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text_message))

    print("Bot is actively polling for incoming messages. Press Ctrl+C to stop.")
    application.run_polling()


if __name__ == "__main__":
    main()
