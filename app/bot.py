from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
from config import telegram_config
from sqlalchemy.orm import Session
from fastapi import Depends
from .database import get_db  # Import the database session dependency
from .crud import create_user  # Import the function to create a user
from .schemas import UserCreate  # Import the user schema
from sqlalchemy.orm import Session
from app.models import User

API_URL = os.getenv("API_URL", "http://localhost:8000")
TG_BOT_TOKEN = os.getenv('TELEGRAM_BOT_API_TOKEN')
print("Bot token:", )

def register_user(db: Session, telegram_id: int, username: str):
    # Check if the user already exists in the database
    existing_user = db.query(User).filter(User.id == telegram_id).first()
    if existing_user:
        return False  # User already registered
    
    # Create a new user in the database
    user = UserCreate(id=telegram_id, name=username)
    create_user(db, user)
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print("Received /start command in chat:", update.message.chat.id)
    keyboard = [
        [InlineKeyboardButton("View Books", callback_data="view_books")],
        [InlineKeyboardButton("Reserve a Book", callback_data="reserve_book")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with buttons
    await update.message.reply_text(
        "Welcome! Please choose an option:",
        reply_markup=reply_markup
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please type something so I can respond")



async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "view_books":
        await query.edit_message_text("Here are some available books...")
    elif query.data == "reserve_book":
        await query.edit_message_text("Please select book to reserve...")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} coused error {context.error}')


def create_bot_app():
    print("Starting bot..")
    bot_app = Application.builder().token(TG_BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CallbackQueryHandler(button_handler))
    
    bot_app.add_error_handler(error)

    print('Polling..')
    bot_app.run_polling(poll_interval=3)