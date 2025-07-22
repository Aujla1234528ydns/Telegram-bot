from telegram import Update
from telegram.helpers import InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

BOT_TOKEN = "7925601385:AAHHRShrFUGuvsllLrrw2koN9vwjNDlejBk"
ADMIN_ID = 5926495978  # Replace if different

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me your feedback (text or image).")

# Handle user messages (text and photo)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.message.chat_id
    msg = update.message

    # Forward text
    if msg.text:
        forward_text = f"📝 Feedback from {user.first_name} ({chat_id}):\n\n{msg.text}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=forward_text)

    # Forward photo
    elif msg.photo:
        file_id = msg.photo[-1].file_id
        caption = f"📷 Photo feedback from {user.first_name} ({chat_id})"
        await context.bot.send_photo(chat_id=ADMIN_ID, photo=file_id, caption=caption)

    await msg.reply_text("✅ Feedback received. Thank you!")

# Reply command for admin to respond
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id != ADMIN_ID:
        return

    try:
        target_id = int(context.args[0])
        reply_msg = " ".join(context.args[1:])
        await context.bot.send_message(chat_id=target_id, text=f"👤 Admin reply:\n{reply_msg}")
        await update.message.reply_text("✅ Message sent to user.")
    except:
        await update.message.reply_text("⚠️ Usage: /reply <user_id> <message>")

# Run bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("reply", reply))
app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))

print("✅ Bot is now running...")
app.run_polling()
