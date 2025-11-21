import unittest
from app import create_app, db
from app.users.models import User
from app import bcrypt

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        # Налаштовуємо додаток для тестування
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_page_loads(self):
        """Перевірка, чи сторінка реєстрації відкривається"""
        response = self.client.get('/users/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Реєстрація".encode('utf-8'), response.data)

    def test_login_page_loads(self):
        """Перевірка, чи сторінка входу відкривається"""
        response = self.client.get('/users/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Вхід".encode('utf-8'), response.data)

    def test_user_registration(self):
        """Тест реєстрації нового користувача"""
        response = self.client.post('/users/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        
        # Перевіряємо, чи користувач зберігся в базі
        user = db.session.scalar(db.select(User).where(User.username == 'testuser'))
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')
        self.assertNotEqual(user.password, 'password123')

    def test_login_logout(self):
        """Тест процедури входу та виходу"""
        # Створюємо користувача вручну
        hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
        user = User(username='loginuser', email='login@example.com', password=hashed_password)
        
        db.session.add(user)
        db.session.commit()

        # 1. Вхід
        response = self.client.post('/users/login', data={
            'email': 'login@example.com',
            'password': 'password'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("Профіль".encode('utf-8'), response.data)
        
        # 2. Вихід
        response = self.client.get('/users/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Вхід".encode('utf-8'), response.data)

if __name__ == '__main__':
    unittest.main()