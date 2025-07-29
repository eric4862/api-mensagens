from flask import Blueprint, request, jsonify
from models import Usuario
from database import db
import re

usuarios_bp = Blueprint('usuarios', __name__)

def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validar_senha(senha):
    return (len(senha) >= 8 and
            re.search(r'[A-Z]', senha) and
            re.search(r'[a-z]', senha) and
            re.search(r'[0-9]', senha) and
            re.search(r'[@!%*?&]', senha))

@usuarios_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.json
    email = dados.get('email')
    nome = dados.get('nome')
    senha = dados.get('senha')

    if not email or not validar_email(email):
        return jsonify({"erro": "Email inválido."}), 400
    if not nome:
        return jsonify({"erro": "Nome é obrigatório."}), 400
    if not senha or not validar_senha(senha):
        return jsonify({"erro": "Senha fraca. Use mínimo 8 caracteres com número, maiúscula, minúscula e especial."}), 400
    if Usuario.query.filter_by(email=email).first():
        return jsonify({"erro": "Email já cadastrado."}), 409

    usuario = Usuario(email=email, nome=nome, senha=senha)
    db.session.add(usuario)
    db.session.commit()
    return jsonify({"id": usuario.id, "email": usuario.email, "nome": usuario.nome}), 201

@usuarios_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([
        {"id": u.id, "email": u.email, "nome": u.nome, "perfil": u.perfil}
        for u in usuarios
    ])

@usuarios_bp.route('/usuarios/<int:id>', methods=['GET'])
def obter_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return jsonify({"id": usuario.id, "email": usuario.email, "nome": usuario.nome, "perfil": usuario.perfil})

@usuarios_bp.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    dados = request.json
    nome = dados.get('nome')
    senha = dados.get('senha')

    if nome:
        usuario.nome = nome
    if senha:
        if not validar_senha(senha):
            return jsonify({"erro": "Senha fraca."}), 400
        usuario.senha = senha

    db.session.commit()
    return jsonify({"id": usuario.id, "email": usuario.email, "nome": usuario.nome})

@usuarios_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"mensagem": "Usuário deletado com sucesso."})
