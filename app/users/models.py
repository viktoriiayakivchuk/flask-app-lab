from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer

# === ВАЖЛИВИЙ БЛОК ===
# Цей імпорт виконається ТІЛЬКИ для перевірки типів (напр. у VS Code),
# але НЕ під час реального запуску програми. Це розриває цикл.
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.posts.models import Post

class User(db.Model):
    __tablename__ = "users" 

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False) 
    posts: Mapped[list["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"