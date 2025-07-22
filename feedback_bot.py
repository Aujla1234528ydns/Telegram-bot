import os
from telegram import Update
from telegram import InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

BOT_TOKEN = os.environ["7925601385:AAHHRShrFUGuvsllLrrw2koN9vwjNDlejBk"]
ADMIN_ID = int(os.environ["5926495978"])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me your feedback (text or image).")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    msg = update.message

    if msg.text:
        forward_text = f"💬 Feedback from {user.first_name} ({chat_id}):\n\n{msg.text}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=forward_text)
    elif msg.photo:
        file_id = msg.photo[-1].file_id
        caption = f"📷 Photo feedback from {user.first_name} ({chat_id})"
        await context.bot.send_photo(chat_id=ADMIN_ID, photo=file_id, caption=caption)

    await msg.reply_text("✅ Feedback received. Thank you!")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.chat_id != ADMIN_ID:
        return

    try:
        args = context.args
        target_id = int(args[0])
        reply_msg = " ".join(args[1:])
        if not reply_msg:
            raise ValueError
        await context.bot.send_message(chat_id=target_id, text=f"🛎 Admin reply:\n{reply_msg}")
        await update.message.reply_text("✅ Message sent to user.")
    except:
        await update.message.reply_text("⚠️ Usage: /reply <user_id> <message>")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", reply))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))
    print("✅ Bot is now running...")
    app.run_polling()
