from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app import db

bp = Blueprint("users", __name__, url_prefix="/users")


# Registrar usuário
@bp.post("")
def register():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email e password são obrigatórios"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email já cadastrado"}), 409

    user = User(email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"id": user.id, "email": user.email}), 201


# Login de usuário
@bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email", "")
    password = data.get("password", "")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Credenciais inválidas"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"access_token": token}), 200


# Listar usuários (rota protegida)
@bp.get("")
@jwt_required()
def list_user():
    _ = get_jwt_identity()  # quem fez a requisição
    users = User.query.with_entities(User.id, User.email).all()

    return jsonify([{"id": u.id, "email": u.email} for u in users])
    