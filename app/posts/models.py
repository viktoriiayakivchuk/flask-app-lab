from datetime import datetime
from .. import db
import enum
from sqlalchemy.orm import Mapped # <<< ВИПРАВЛЕННЯ 1: Імпортуємо Mapped

class PostCategory(enum.Enum):
    # ... (інша частина коду enum залишається без змін)
    news = 'news'
    publication = 'publication'
    tech = 'tech'
    other = 'other'

class Post(db.Model):
    """
    ORM-модель Post, оновлена до стилю Flask-SQLAlchemy 2.0+.
    """
    __tablename__ = 'posts'
    
    # ВИПРАВЛЕННЯ 2: Використовуємо Mapped замість db.Mapped
    id: Mapped[int] = db.mapped_column(primary_key=True)
    
    title: Mapped[str] = db.mapped_column(
        db.String(150), nullable=False
    )
    
    content: Mapped[str] = db.mapped_column(
        db.Text, nullable=False
    )
    
    posted: Mapped[datetime] = db.mapped_column(
        default=datetime.utcnow
    )
    
    category: Mapped[PostCategory] = db.mapped_column(
        db.Enum(PostCategory)
    )
    
    is_active: Mapped[bool] = db.mapped_column(
        default=True
    )
    
    author: Mapped[str] = db.mapped_column(
        db.String(20), default='Anonymous'
    )
    
    def __repr__(self):
        # ... (інша частина коду залишається без змін)
        return f"<Post(id={self.id}, title='{self.title}', author='{self.author}')>"