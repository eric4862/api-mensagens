from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Mensagem
from database import db

mensagens_bp = Blueprint('mensagens', __name__)

# Função para verificar se é admin
def verificar_admin(identidade):
    if identidade['perfil'] != 'ADMIN':
        return jsonify({"erro": "Apenas administradores têm acesso."}), 403
    return None

@mensagens_bp.route('/mensagens', methods=['POST'])
@jwt_required()
def criar_mensagem():
    identidade = get_jwt_identity()
    conteudo = request.json.get('conteudo')
    if not conteudo:
        return jsonify({"erro": "Conteúdo é obrigatório."}), 400

    nova = Mensagem(conteudo=conteudo, autor_id=identidade['id'])
    db.session.add(nova)
    db.session.commit()

    return jsonify({
        "id": nova.id,
        "conteudo": nova.conteudo,
        "autor_id": nova.autor_id
    }), 201

@mensagens_bp.route('/mensagens', methods=['GET'])
def listar_mensagens():
    mensagens = Mensagem.query.all()
    return jsonify([
        {
            "id": msg.id,
            "conteudo": msg.conteudo,
            "autor_id": msg.autor_id
        } for msg in mensagens
    ])

@mensagens_bp.route('/mensagens/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_mensagem(id):
    identidade = get_jwt_identity()
    msg = Mensagem.query.get_or_404(id)

    if msg.autor_id != identidade['id']:
        return jsonify({"erro": "Você só pode editar suas próprias mensagens."}), 403

    novo_conteudo = request.json.get('conteudo')
    if not novo_conteudo:
        return jsonify({"erro": "Conteúdo é obrigatório."}), 400

    msg.conteudo = novo_conteudo
    db.session.commit()
    return jsonify({"mensagem": "Atualizada com sucesso!"})

@mensagens_bp.route('/mensagens/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_mensagem(id):
    identidade = get_jwt_identity()
    msg = Mensagem.query.get_or_404(id)

    # Só o autor ou um ADMIN pode deletar
    if msg.autor_id != identidade['id'] and identidade['perfil'] != 'ADMIN':
        return jsonify({"erro": "Apenas o autor ou um administrador pode excluir."}), 403

    db.session.delete(msg)
    db.session.commit()
    return jsonify({"mensagem": "Mensagem excluída com sucesso."})
