from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import sqlite3
from config import TOKEN

# Database
conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    cur.execute(
        "INSERT OR IGNORE INTO users(user_id, balance) VALUES (?, ?)",
        (user.id, 0)
    )
    conn.commit()

    keyboard = [
        ["💰 Wallet"],
        ["🎲 Dice", "🪙 Coin Flip"],
        ["🎰 Spin", "🎯 Guess"]
    ]

    await update.message.reply_text(
        f"👋 Welcome {user.first_name}!",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user

    if text == "💰 Wallet":
        cur.execute(
            "SELECT balance FROM users WHERE user_id=?",
            (user.id,)
        )
        row = cur.fetchone()
        balance = row[0] if row else 0
        await update.message.reply_text(
            f"💰 আপনার ব্যালেন্স: {balance} টাকা"
        )

    elif text == "🎲 Dice":
        await update.message.reply_dice()

    elif text == "🪙 Coin Flip":
        await update.message.reply_text("🚧 Coin Flip শীঘ্রই আসছে!")

    elif text == "🎰 Spin":
        await update.message.reply_text("🚧 Spin Wheel শীঘ্রই আসছে!")

    elif text == "🎯 Guess":
        await update.message.reply_text("🚧 Guess Game শীঘ্রই আসছে!")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, menu)
)

print("✅ Bot Running...")
app.run_polling()
