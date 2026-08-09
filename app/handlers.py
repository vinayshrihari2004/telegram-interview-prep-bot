from telegram import Update
from telegram.ext import ContextTypes

from database import SessionLocal
from models import User
from crud import get_random_question

async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE):

    db = SessionLocal()

    try:
        telegram_id = str(update.effective_user.id)
        username = update.effective_user.username
        name = update.effective_user.first_name

        existing_user = (
            db.query(User)
            .filter(User.telegram_id == telegram_id)
            .first()
        )

        if not existing_user:
            user = User(
                telegram_id=telegram_id,
                username=username,
                name=name
            )

            db.add(user)
            db.commit()

        await update.message.reply_text(
            f"Welcome {name}! 🚀\n\nInterview Prep Bot is ready."
        )

    finally:
        db.close()

async def question(update, context):

    q = get_random_question()

    if not q:
        await update.message.reply_text(
            "No questions found in database."
        )
        return

    await update.message.reply_text(
        f"📚 Category: {q.category}\n\n"
        f"❓ Question:\n{q.question}"
    )

async def question(update, context):
    q = get_random_question()

    if not q:
        await update.message.reply_text(
            "No questions found."
        )
        return

    context.user_data["answer"] = q.answer

    await update.message.reply_text(
        f"📚 Category: {q.category}\n\n"
        f"❓ Question:\n{q.question}\n\n"
        f"Type /answer"
    )

async def answer(update, context):

    answer = context.user_data.get("answer")

    if not answer:
        await update.message.reply_text(
            "Ask a question first using /question"
        )
        return

    await update.message.reply_text(
        f"✅ Answer:\n\n{answer}"
    )