from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes



BOT_TOKEN = "8296663214:AAGnEF1TEhy4KKhE5TUWy2YN4K6AxMTVQKk"      
ADMIN_ID = 7080287669                 
CHANNEL_LINK = "https://t.me/+obsenlGQQC4wMzI6" 



START_MESSAGE = (
    "👋 Привет! Я *Ассистент Подпольного Собрания.*\n\n"
    "📩 Сюда ты можешь отправить задание, которое нужно разобрать или получить ответы.\n"
    "⚙️ Будь готов, что не все задания мы публикуем в канал.\n\n"
    "_Выбери действие ниже:_"
)

HELP_TEXT = (
    "ℹ️ Просто отправь сюда текст или фото своего задания.\n"
    "Мы получим его и передадим менеджеру для разбора.\n\n"
    "⬅️ Нажми «Назад в меню», чтобы вернуться."
)

ABOUT_TEXT = (
    f"📢 Наш канал: {CHANNEL_LINK}\n\n"
    "🕵️ Здесь публикуются ответы, примеры и пояснения.\n"
    "⬅️ Нажми «Назад в меню», чтобы вернуться."
)

THANK_YOU_TEXT = "✅ Ваша задача принята в работу, спасибо за обращение к нам!"



MAIN_MENU = [
    ["📤 Отправить задание"],
    ["🆘 Помощь", "📢 О канале"]
]

BACK_MENU = [
    ["⬅️ Назад в меню"]
]



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    await update.message.reply_text(
        START_MESSAGE,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📤 Отправить задание":
        await update.message.reply_text(
            "✉️ Пришли сюда своё задание (текст или фото), и мы примем его в работу.",
            reply_markup=ReplyKeyboardMarkup(BACK_MENU, resize_keyboard=True)
        )

    elif text == "🆘 Помощь":
        await update.message.reply_text(HELP_TEXT, reply_markup=ReplyKeyboardMarkup(BACK_MENU, resize_keyboard=True))

    elif text == "📢 О канале":
        await update.message.reply_text(ABOUT_TEXT, reply_markup=ReplyKeyboardMarkup(BACK_MENU, resize_keyboard=True))

    elif text == "⬅️ Назад в меню":
        await update.message.reply_text(
            "🔙 Возвращаемся в главное меню.",
            reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        )

    else:
        
        await forward_to_admin(update, context)

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        if update.message.photo:
            
            file_id = update.message.photo[-1].file_id
            caption = update.message.caption or ""
            await context.bot.send_photo(chat_id=ADMIN_ID, photo=file_id, caption=f"📩 От @{user.username or user.first_name}:\n{caption}")
        else:
            
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"📩 От @{user.username or user.first_name}:\n{update.message.text}")

        await update.message.reply_text(THANK_YOU_TEXT)

    except Exception as e:
        print(f"Ошибка пересылки: {e}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_buttons))

    print("✅ Бот запущен и готов к работе!")
    app.run_polling()

if __name__ == "__main__":
    main()
