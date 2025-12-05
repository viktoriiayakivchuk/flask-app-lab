from datetime import datetime 
from app import db, bcrypt, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime 
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.posts.models import Post
    from app.expenses.models import Expense

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "users" 

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    image: Mapped[str] = mapped_column(String(20), nullable=True, default='profile_default.jpg')
    about_me: Mapped[str | None] = mapped_column(String(140), nullable=True) 
    last_seen: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    posts: Mapped[list["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    expenses: Mapped[list["Expense"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)