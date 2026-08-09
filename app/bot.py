from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN
from handlers import start, question, answer

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("question", question))
app.add_handler(CommandHandler("answer", answer))
print("Bot Running...")
app.run_polling()