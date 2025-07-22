import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Load environment variables
BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send your feedback here.")

# Handle text or photo messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    # Handle text
    if update.message.text:
        message = f"Feedback from @{user.username or user.first_name} (ID: {chat_id}):\n{update.message.text}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=message)
        await update.message.reply_text("✅ Feedback sent!")

    # Handle photo
    elif update.message.photo:
        caption = update.message.caption or "(no caption)"
        photo_file = update.message.photo[-1]
        await photo_file.get_file().download_to_drive("feedback.jpg")
        await context.bot.send_photo(chat_id=ADMIN_ID, photo=open("feedback.jpg", "rb"), caption=f"From @{user.username or user.first_name}:\n{caption}")
        await update.message.reply_text("✅ Photo feedback sent!")

# Main function
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))

    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
