from app.models import User
from flask_jwt_extended import create_access_token
from app import db

def create_user(email, password):
    # cria novo usuário e salva no banco
    user = User(email=email)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    return user

def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        # retorna um JWT válido
        return create_access_token(identity=user.id)
    return None