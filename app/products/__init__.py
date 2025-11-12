# app/products/__init__.py
from flask import Blueprint

products_bp = Blueprint("products", __name__, url_prefix="/products")

# опційно — тестовий маршрут, щоби швидко перевірити
@products_bp.get("/")
def index():
    return "Products OK"

