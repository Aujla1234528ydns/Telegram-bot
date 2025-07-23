import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Load bot token and admin ID from environment variables
BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Please send your feedback.")

# Handle all messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    # Handle text feedback
    if update.message.text:
        msg = f"📝 Feedback from @{user.username or user.first_name} (ID: {chat_id}):\n\n{update.message.text}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
        await update.message.reply_text("✅ Your message has been sent!")

    # Handle photo feedback
    elif update.message.photo:
        caption = update.message.caption or "(No caption)"
        photo_file = update.message.photo[-1]
        file = await photo_file.get_file()
        await file.download_to_drive("photo.jpg")
        with open("photo.jpg", "rb") as photo:
            await context.bot.send_photo(chat_id=ADMIN_ID, photo=photo, caption=f"📸 From @{user.username or user.first_name}:\n{caption}")
        await update.message.reply_text("✅ Your photo has been sent!")

# Main function
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))

    print("Bot is running...")
    await app.run_polling()

# Entry point
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
