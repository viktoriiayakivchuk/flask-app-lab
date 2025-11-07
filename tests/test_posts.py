import unittest
from app import create_app, db
# Імпортуємо обидві моделі, бо PostCategory потрібен для 'category'
from app.posts.models import Post, PostCategory 
from datetime import datetime

class PostModelTestCase(unittest.TestCase):
    """
    Оновлений клас для тестування вашої нової моделі Post.
    """

    def setUp(self):
        self.app = create_app(config_name="test")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_post_creation(self):
        """
        Тест: перевіряємо, чи створюється пост з 'content' та Enum.
        """
        # 1. Створюємо екземпляр поста з 'content' (замість 'body')
        p = Post(
            title="Test Post", 
            content="This is the content of a test post.", # <--- ВИПРАВЛЕННЯ
            category=PostCategory.tech # Використовуємо Enum
        )
        
        db.session.add(p)
        db.session.commit()
        
        retrieved_post = db.session.scalar(
            db.select(Post).where(Post.title == "Test Post")
        )
        
        # 4. Перевіряємо, чи це той самий пост
        self.assertIsNotNone(retrieved_post)
        self.assertEqual(retrieved_post.title, "Test Post")
        self.assertEqual(retrieved_post.content, "This is the content of a test post.")
        self.assertEqual(retrieved_post.category, PostCategory.tech)
        self.assertIsInstance(retrieved_post.posted, datetime)

    def test_repr(self):
        """
        Тест: перевіряємо метод __repr__
        """
        # Використовуємо 'content' (замість 'body')
        p = Post(title="Test Repr", content="body")
        db.session.add(p)
        db.session.commit()
        
        test_id = p.id 
        
        # Перевіряємо, чи __repr__ відповідає вашій моделі
        self.assertEqual(
            repr(p), 
            f"<Post(id={test_id}, title='Test Repr', author='Anonymous')>"
        )

    def test_default_values(self):
        """
        Тест: перевіряємо, чи працюють 'default' у моделі
        """
        p = Post(title="Default Test", content="body", category=PostCategory.news)
        db.session.add(p)
        db.session.commit()
        
        retrieved_post = db.get_or_404(Post, p.id)
        
        # Перевіряємо 'default' з вашої моделі
        self.assertEqual(retrieved_post.author, 'Anonymous')
        self.assertEqual(retrieved_post.is_active, True)