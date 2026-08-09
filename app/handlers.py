from telegram import Update
from telegram.ext import ContextTypes

from database import SessionLocal
from models import User

from crud import (
    get_random_question,
    get_question_by_id
)

from crud import (
    set_user_category,
    get_user_category,
    get_random_question_by_category
)


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    db = SessionLocal()

    try:
        telegram_id = str(update.effective_user.id)
        username = update.effective_user.username
        name = update.effective_user.first_name

        existing_user = (
            db.query(User)
            .filter(
                User.telegram_id == telegram_id
            )
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
                f"Welcome {name}! 🚀\n\n"
                f"No category selected.\n\n"
                f"Choose a category:\n"
                f"/python\n"
                f"/dbms"
            )

        else:

            category = existing_user.selected_category

            if category:

                await update.message.reply_text(
                    f"Welcome {name}! 🚀\n\n"
                    f"Current Category: {category}\n\n"
                    f"Use:\n"
                    f"/python - Switch to Python\n"
                    f"/dbms - Switch to DBMS\n\n"
                    f"Type /question to start practicing."
                )

            else:

                await update.message.reply_text(
                    f"Welcome {name}! 🚀\n\n"
                    f"No category selected.\n\n"
                    f"Choose a category:\n"
                    f"/python\n"
                    f"/dbms"
                )

    finally:
        db.close()

async def question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    telegram_id = str(
        update.effective_user.id
    )

    category = get_user_category(
        telegram_id
    )

    if not category:

        await update.message.reply_text(
            "Choose a category first.\n\n"
            "/python\n"
            "/dbms"
        )

        return

    q = get_random_question_by_category(
        category
    )

    if not q:

        await update.message.reply_text(
            f"No questions found in {category} category."
        )

        return

    context.user_data[
        "current_question_id"
    ] = q.id

    await update.message.reply_text(
        f"📚 Category: {q.category}\n\n"
        f"❓ Question:\n{q.question}\n\n"
        f"Type your answer below 👇"
    )


async def check_answer(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    question_id = context.user_data.get(
        "current_question_id"
    )

    if not question_id:
        return

    q = get_question_by_id(question_id)

    if not q:
        await update.message.reply_text(
            "Question not found."
        )
        return

    user_answer = (
        update.message.text
        .strip()
        .lower()
    )

    correct_answer = (
        q.answer
        .strip()
        .lower()
    )

    if is_answer_correct(
        user_answer,
        correct_answer
    ):
        await update.message.reply_text(
            "✅ Correct!"
        )

    else:
        await update.message.reply_text(
            f"❌ Incorrect\n\n"
            f"✅ Correct Answer:\n{q.answer}"
        )

    context.user_data.pop(
        "current_question_id",
        None
    )


def is_answer_correct(
    user_answer,
    correct_answer
):
    user_words = set(
        user_answer.split()
    )

    correct_words = set(
        correct_answer.split()
    )

    common_words = (
        user_words &
        correct_words
    )

    score = (
        len(common_words)
        / len(correct_words)
    )

    return score >= 0.5

async def python_category(
    update,
    context
):
    telegram_id = str(
        update.effective_user.id
    )

    set_user_category(
        telegram_id,
        "Python"
    )

    await update.message.reply_text(
        "🐍 Category set to Python"
    )

async def dbms_category(
    update,
    context
):
    telegram_id = str(
        update.effective_user.id
    )

    set_user_category(
        telegram_id,
        "DBMS"
    )

    await update.message.reply_text(
        "🗄️ Category set to DBMS"
    )