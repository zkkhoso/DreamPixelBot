import os
import openai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

openai.api_key = os.getenv("OPENAI_API_KEY")
user_states = {}

styles = {
    "ghibli": "in Studio Ghibli style",
    "realistic": "as a realistic photo",
    "anime": "in anime style",
    "cyberpunk": "in cyberpunk art style",
    "sketch": "as a pencil sketch",
    "oil": "as an oil painting"
}

sizes = ["256x256", "512x512", "1024x1024"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to AI Image Bot!\nUse /styles to select an image style and start generating images!"
    )

async def styles_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(style.capitalize(), callback_data=key)] for key, style in styles.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose an image style:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    style_key = query.data
    user_states[query.from_user.id] = {"style": style_key}
    await query.message.reply_text(f"You chose *{style_key}* style. Now send your prompt.", parse_mode="Markdown")

async def handle_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_states or "style" not in user_states[user_id]:
        await update.message.reply_text("Please use /styles to choose a style first.")
        return

    prompt = update.message.text
    chosen_style = styles[user_states[user_id]["style"]]
    full_prompt = f"{prompt}, {chosen_style}"

    await update.message.reply_text("Generating images... please wait.")

    for size in sizes:
        try:
            response = openai.images.generate(
                model="dall-e-3",
                prompt=full_prompt,
                size=size,
                n=1,
            )
            image_url = response.data[0].url
            await update.message.reply_photo(photo=image_url, caption=f"Size: {size}")
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")

def main():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("styles", styles_command))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_prompt))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
