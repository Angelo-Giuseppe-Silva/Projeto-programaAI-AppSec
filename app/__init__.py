from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "sua_chave_super_secreta"  # troque depois!

    db.init_app(app)
    jwt.init_app(app)

    # Registrar blueprints
    from app.routes.users import bp as users_bp
    app.register_blueprint(users_bp)

    with app.app_context():
        db.create_all()

    return app