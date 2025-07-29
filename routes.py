from flask import Blueprint, request, jsonify
from models import Mensagem
from database import db

mensagens_bp = Blueprint('mensagens', __name__)

@mensagens_bp.route('/mensagens', methods=['POST'])
def criar_mensagem():
    conteudo = request.json.get('conteudo')
    if not conteudo:
        return jsonify({"erro": "Conteúdo é obrigatório."}), 400
    msg = Mensagem(conteudo=conteudo)
    db.session.add(msg)
    db.session.commit()
    return jsonify({"id": msg.id, "conteudo": msg.conteudo}), 201

@mensagens_bp.route('/mensagens', methods=['GET'])
def listar_mensagens():
    mensagens = Mensagem.query.all()
    return jsonify([{"id": m.id, "conteudo": m.conteudo} for m in mensagens])

@mensagens_bp.route('/mensagens/<int:id>', methods=['GET'])
def obter_mensagem(id):
    msg = Mensagem.query.get_or_404(id)
    return jsonify({"id": msg.id, "conteudo": msg.conteudo})

@mensagens_bp.route('/mensagens/<int:id>', methods=['PUT'])
def atualizar_mensagem(id):
    msg = Mensagem.query.get_or_404(id)
    conteudo = request.json.get('conteudo')
    if not conteudo:
        return jsonify({"erro": "Conteúdo é obrigatório."}), 400
    msg.conteudo = conteudo
    db.session.commit()
    return jsonify({"id": msg.id, "conteudo": msg.conteudo})

@mensagens_bp.route('/mensagens/<int:id>', methods=['DELETE'])
def deletar_mensagem(id):
    msg = Mensagem.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    return jsonify({"mensagem": "Mensagem deletada."})
