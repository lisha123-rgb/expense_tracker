from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Numeric

# -------------------------
# USER LOADER (SAFE)
# -------------------------
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except (TypeError, ValueError):
        return None


# -------------------------
# USER MODEL
# -------------------------
class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
        index=True
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.String(256),   # Increased size for safety
        nullable=False
    )

    # Cascade delete prevents orphaned expenses
    expenses = db.relationship(
        "Expense",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# -------------------------
# CATEGORY MODEL
# -------------------------
class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
        index=True
    )

    expenses = db.relationship(
        "Expense",
        back_populates="category",
        cascade="all, delete-orphan",
        lazy=True
    )


# -------------------------
# EXPENSE MODEL
# -------------------------
class Expense(db.Model):
    __tablename__ = "expense"

    id = db.Column(db.Integer, primary_key=True)

    # Financial precision fix
    amount = db.Column(
        Numeric(10, 2),
        nullable=False
    )

    description = db.Column(
        db.String(200),
        nullable=False
    )

    date = db.Column(
        db.Date,
        nullable=False,
        index=True
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id", ondelete="CASCADE"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    category = db.relationship("Category", back_populates="expenses")
    user = db.relationship("User", back_populates="expenses")
