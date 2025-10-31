from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# === НАСТРОЙКИ ===
BOT_TOKEN = "8296663214:AAGnEF1TEhy4KKhE5TUWy2YN4K6AxMTVQKk"
ADMIN_CHAT_ID = 7080287669  # Кому бот пересылает сообщения

# === ФУНКЦИЯ /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Привет, я ассистент Подпольного собрания.\n"
        "Сюда ты можешь отправить задание, которое надо разобрать или получить ответы.\n"
        "Будь готов, что не все задания мы публикуем в канал."
    )
    await update.message.reply_text(welcome_text)

# === ОБРАБОТКА ВСЕХ СООБЩЕНИЙ ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"📩 Получено сообщение от @{update.message.from_user.username}: {update.message.text if update.message.text else 'фото/файл'}")
    print(f"🆔 chat_id = {update.message.chat.id}")
    user = update.message.from_user
    text = update.message.text
    photo = update.message.photo

    # Получаем ID администратора
    try:
        chat_admin = await context.bot.get_chat(ADMIN_CHAT_ID)
        admin_id = chat_admin.id
    except Exception as e:
        print("Ошибка получения ID администратора:", e)
        return

    # Отправляем сообщение админу
    if photo:
        file_id = photo[-1].file_id  # лучшее качество
        caption = update.message.caption or "(без подписи)"
        await context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=file_id,
                                     caption=f"📩 От @{user.username or user.id}:\n{caption}")
    elif text:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID,
                                       text=f"📩 От @{user.username or user.id}:\n{text}")
    else:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID,
                                       text=f"📩 От @{user.username or user.id}: (неизвестный тип сообщения)")

    # Отвечаем пользователю
    await update.message.reply_text("Ваша задача принята в работу, спасибо за обращение к нам ✅")

# === ЗАПУСК БОТА ===
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))

print("🤖 Бот запущен...")
app.run_polling()
