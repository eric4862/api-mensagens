from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models import Usuario
from database import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')

    user = Usuario.query.filter_by(email=email).first()
    if not user or user.senha != senha:
        return jsonify({"erro": "Credenciais inválidas"}), 401

    access_token = create_access_token(identity={"id": user.id, "perfil": user.perfil})
    refresh_token = create_refresh_token(identity={"id": user.id, "perfil": user.perfil})

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    })

@auth_bp.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identidade = get_jwt_identity()
    novo_access = create_access_token(identity=identidade)
    return jsonify({"access_token": novo_access})
