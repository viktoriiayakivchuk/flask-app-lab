from datetime import datetime
from .. import db
import enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column, Integer, String, Text, Enum, Boolean, DateTime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.users.models import User

# Асоціативна таблиця 
post_tags = Table(
    'post_tags',
    db.metadata, 
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class PostCategory(enum.Enum):
    news = 'news'
    publication = 'publication'
    tech = 'tech'
    other = 'other'

# НОВА МОДЕЛЬ
class Tag(db.Model):
    __tablename__ = 'tags'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    # Зворотний зв'язок до Post
    posts: Mapped[list["Post"]] = relationship(
        secondary=post_tags, 
        back_populates="tags"
    )
    
    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}')>"

class Post(db.Model):
    __tablename__ = 'posts'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    category: Mapped[PostCategory] = mapped_column(Enum(PostCategory))
    is_active: Mapped[bool] = mapped_column(default=True)
    
    # Зв'язок One-to-Many (з пункту 3)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")

    # Зв'язок Many-to-Many
    tags: Mapped[list["Tag"]] = relationship(
        secondary=post_tags, 
        back_populates="posts"
    )

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', user_id='{self.user_id}')>"