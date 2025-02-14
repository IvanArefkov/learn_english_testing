from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, JSON
from database import db
from flask_login import UserMixin


# ==============================
# 1️⃣ User Table (Students & Teachers)
# ==============================
class User(UserMixin,db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False, default="student")  # student, teacher, admin
    grade_level: Mapped[int] = mapped_column(nullable=True)  # Grade level for students
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password,method="scrypt", salt_length=8)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name} - {self.role}>'


# ==============================
# 2️⃣ ExamQuestion Table (Stores All Questions)
# ==============================
class Examquestion(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(nullable=False)  # reading, grammar, writing, vocabulary
    type: Mapped[str] = mapped_column(nullable=False)  # multiple_choice, fill_in_blank, essay_prompt
    difficulty: Mapped[int] = mapped_column(nullable=False)  # Difficulty level (1-3)
    question_text: Mapped[str] = mapped_column(nullable=False)
    correct_answer: Mapped[str] = mapped_column(nullable=False)  # Correct answer (string)
    incorrect_answers: Mapped[dict] = mapped_column(JSON, nullable=True)  # Store multiple choice options
    explanation: Mapped[str] = mapped_column(nullable=True)  # Explanation for correct answer
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    def __repr__(self):
        return f'<ExamQuestion {self.id} - {self.category}>'


# ==============================
# 3️⃣ TestSessions Table (Tracks Full Test Attempts)
# ==============================
class Testsession(db.Model):
    session_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    mode: Mapped[str] = mapped_column(nullable=False)  # exam, practice, targeted
    category_filter: Mapped[str] = mapped_column(nullable=True)  # If focused on one category
    started_at: Mapped[datetime] = mapped_column(default=datetime.now)
    completed_at: Mapped[datetime] = mapped_column(nullable=True)  # Null if test is unfinished
    status: Mapped[str] = mapped_column(nullable=False, default="in_progress")  # in_progress, submitted, reviewed

    user = relationship('User', backref=db.backref('testsessions', lazy=True))

    def __repr__(self):
        return f'<TestSession {self.session_id} - {self.user_id} - {self.status}>'


# ==============================
# 4️⃣ TestAnswers Table (Stores User Answers in Each Test Session)
# ==============================
class Testanswer(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey('testsession.session_id'), nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey('examquestion.id'), nullable=False)
    user_answer: Mapped[str] = mapped_column(nullable=False)  # User's answer (essay, MCQ, etc.)
    is_correct: Mapped[bool] = mapped_column(nullable=True)  # Null for essays (requires manual grading)
    score: Mapped[float] = mapped_column(nullable=True)  # Score assigned (used for essays)
    answered_at: Mapped[datetime] = mapped_column(default=datetime.now)

    session = relationship('Testsession', backref=db.backref('answers', lazy=True))
    question = relationship('Examquestion', backref=db.backref('answers', lazy=True))

    def __repr__(self):
        return f'<TestAnswer {self.id} - Session {self.session_id}>'


# ==============================
# 5️⃣ TestScores Table (Stores Final Results for Each Test Attempt)
# ==============================
class Testscore(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey('testsession.session_id'), nullable=False)
    total_questions: Mapped[int] = mapped_column(nullable=False)
    correct_answers: Mapped[int] = mapped_column(nullable=False)
    accuracy: Mapped[float] = mapped_column(nullable=False)  # Percentage score
    graded_at: Mapped[datetime] = mapped_column(default=datetime.now)
    reviewed_by: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True)  # Teacher who reviewed essay questions

    session = relationship('Testsession', backref=db.backref('testscores', lazy=True))

    def __repr__(self):
        return f'<Testscore {self.session_id} - {self.accuracy}%>'


# ==============================
# 6️⃣ UserProgress Table (Tracks User Performance Across Multiple Tests)
# ==============================
class Userprogress(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)  # Tracks progress per category
    total_attempts: Mapped[int] = mapped_column(nullable=False, default=0)
    correct_attempts: Mapped[int] = mapped_column(nullable=False, default=0)
    accuracy: Mapped[float] = mapped_column(nullable=False, default=0.0)  # % accuracy

    user = relationship('User', backref=db.backref('progress', lazy=True))

    def __repr__(self):
        return f'<Userprogress {self.user_id} - {self.category}>'


