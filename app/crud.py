from database import SessionLocal
from models import InterviewQuestion
from sqlalchemy.sql.expression import func
from models import User

def get_random_question():
    db = SessionLocal()

    try:
        question = (
            db.query(InterviewQuestion)
            .order_by(func.random())
            .first()
        )

        return question

    finally:
        db.close()


def get_question_by_id(question_id):

    db = SessionLocal()

    try:
        return (
            db.query(InterviewQuestion)
            .filter(
                InterviewQuestion.id == question_id
            )
            .first()
        )

    finally:
        db.close()

def set_user_category(
    telegram_id,
    category
):
    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(
                User.telegram_id == telegram_id
            )
            .first()
        )

        if user:
            user.selected_category = category
            db.commit()

    finally:
        db.close()

def get_user_category(
    telegram_id
):
    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(
                User.telegram_id == telegram_id
            )
            .first()
        )

        if user:
            return user.selected_category

        return None

    finally:
        db.close()

def get_random_question_by_category(category):
    db = SessionLocal()

    try:
        question = (
            db.query(InterviewQuestion)
            .filter(
                InterviewQuestion.category == category
            )
            .order_by(func.random())
            .first()
        )

        return question

    finally:
        db.close()