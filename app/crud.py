from database import SessionLocal
from models import InterviewQuestion
from sqlalchemy.sql.expression import func

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