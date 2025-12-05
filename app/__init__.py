from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from .config import config_map 
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from flask_migrate import Migrate
from .extensions import bcrypt, login_manager 
import os

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app(config_name: str = os.environ.get("FLASK_CONFIG", "dev")) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])
    
    print(f"Running in config: {config_name}")

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'users_bp.login' 
    login_manager.login_message = 'Будь ласка, увійдіть, щоб отримати доступ до цієї сторінки.'
    login_manager.login_message_category = 'info'

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    with app.app_context():
        from . import views as main_blueprint
        app.register_blueprint(main_blueprint.main_bp)
        
        from .users.views import users_bp
        app.register_blueprint(users_bp)
        
        from .posts import post_bp
        app.register_blueprint(post_bp, url_prefix="/posts")

        
        from .products import products_bp
        app.register_blueprint(products_bp)   

        from .expenses import expenses_bp
        app.register_blueprint(expenses_bp)

        from .products import models

        from .posts import models 
        from .users import models
        from .expenses import models

    return app