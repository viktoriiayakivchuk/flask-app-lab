# app/users/models.py
from app import db, bcrypt, login_manager # <--- Додаємо імпорти
from flask_login import UserMixin # <--- Імпорт UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.posts.models import Post

# === UserLoader (потрібен для Flask-Login) ===
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): # <--- Додаємо UserMixin
    __tablename__ = "users" 

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False) 
    
    posts: Mapped[list["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
    
    # === Методи для роботи з паролем (рекомендація методички) ===
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)