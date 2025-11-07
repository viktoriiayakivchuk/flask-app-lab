from app import create_app
import os

# Зчитуємо FLASK_CONFIG з .env, за замовчуванням 'dev'
config_name = os.environ.get("FLASK_CONFIG", "dev")

app = create_app(config_name)

if __name__ == "__main__":
    app.run()