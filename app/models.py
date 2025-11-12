from app import db  # Імпортуємо 'db' з app/__init__.py
from datetime import datetime, timezone

class Post(db.Model):
    """
    Модель для збереження постів у блозі.
    """
    __tablename__ = 'posts' # Явно вказуємо назву таблиці
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        """
        Метод, який повертає рядок для представлення об'єкта (наприклад, у консолі).
        """
        return f'<Post {self.id}: {self.title}>'