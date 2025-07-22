# Telegram Feedback Bot

## Setup

1. Create a Telegram bot using @BotFather and get your `BOT_TOKEN`.
2. Get your Telegram numeric `ADMIN_ID` from @userinfobot.
3. Set environment variables on Render:
   - `BOT_TOKEN=your_token_here`
   - `ADMIN_ID=your_id_here`

## Render Deployment

- Build Command: `pip install -r requirements.txt`
- Start Command: `python feedback_bot.py`
- Runtime: Defined in `runtime.txt`