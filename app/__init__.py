from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

login_manager.login_view = "main.login"
login_manager.session_protection = "strong"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    # ✅ Create tables automatically (production safe)
    with app.app_context():
        db.create_all()

        from app.models import Category

        default_categories = [
            "Food",
            "Travel",
            "Shopping",
            "Bills",
            "Entertainment",
            "Others"
        ]

        for name in default_categories:
            if not Category.query.filter_by(name=name).first():
                db.session.add(Category(name=name))

        db.session.commit()

    return app

















