from http.client import responses

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
from httpx import AsyncClient


# API_URL = os.getenv("API_URL", "http://localhost:8000")
# TG_BOT_TOKEN = os.getenv('TELEGRAM_BOT_API_TOKEN')
TG_BOT_TOKEN = "7163396769:AAH_7SEd2aufZanCKZDa8gwOo-CwYxDIV0s"
app_client = AsyncClient(base_url="http://localhost:8000")

async def handle_reservation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    book_id = query.data.split(":")[1]
    user_id = query.from_user.id

    payload = {
        "user_id": user_id,
        "book_id": book_id
    }

    async with app_client as ac:
        response = await ac.post("/reservations/", json=payload)
        if response.status_code == 400:
            await query.message.reply_text(response.json().get("detail", "Failed to reserve book."))
        else:
            await query.message.reply_text("Book reserved successfully!")

async def handle_book_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    book_id = query.data.split(":")[1]
    async with app_client as ac:
        response = await ac.get(f"/books/{book_id}")
        if response.status_code == 404:
            await update.message.reply_text("Book not found.")
        else:
            book = response.json()
            message = (
                f"**Title:** {book['title']}\n"
                f"**Author:** {book['author']}\n"
                f"**Genre:** {book['genre']}\n"
                f"**Description:** {book['description'] or 'No description provided.'}\n"
                f"**Status:** {'Available' if book['status'] == 'available' else 'Not available'}"
            )
        keyboard = [[InlineKeyboardButton("Reserve", callback_data=f"reserve:{book_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(message, reply_markup=reply_markup)

async def search_books(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args) if context.args else ""
    page = 1

    async with app_client as ac:
        response = await ac.get(f"/books?search={query}&page={page}&size=5")
        if response.status_code != 200:
            await update.message.reply_text("Error fetching books.")
            return

        books = response.json()
        if not books:
            await update.message.reply_text("No books found.")
            return

        # Create Buttons for each book
        keyboard = [
            [InlineKeyboardButton(book['title'], callback_data=f"book_details:{book['id']}")]
            for book in books
        ]
        keyboard.append([InlineKeyboardButton("Next page", callback_data=f"search:{query}:{page + 1}")])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Select a book", reply_markup=reply_markup)


def create_bot_app():
    print("Starting bot...")
    # create application with token
    bot_app = Application.builder().token(TG_BOT_TOKEN).build()

    # register commands
    # bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("search_books", search_books))

    # Register callback query handlers for inline buttons
    bot_app.add_handler(CallbackQueryHandler(handle_book_details, pattern="^book_details:"))
    bot_app.add_handler(CallbackQueryHandler(handle_reservation, pattern="^reserve:"))
    bot_app.add_handler(CallbackQueryHandler(search_books, pattern="^search:"))

    print('Polling..')
    bot_app.run_polling(poll_interval=3, verify=False)