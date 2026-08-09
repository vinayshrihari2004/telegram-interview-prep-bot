from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN
from handlers import start, question,check_answer,python_category,dbms_category
from telegram.ext import MessageHandler, filters
from handlers import (
    start,
    question,
    check_answer,
    python_category,
    dbms_category,
    stats
)

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("question", question))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        check_answer
    )
)

app.add_handler(
    CommandHandler(
        "python",
        python_category
    )
)

app.add_handler(
    CommandHandler(
        "dbms",
        dbms_category
    )
)

app.add_handler(
    CommandHandler(
        "stats",
        stats
    )
)

print("Bot Running...")
app.run_polling()