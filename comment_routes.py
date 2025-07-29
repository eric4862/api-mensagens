from flask import Blueprint, request, jsonify
from models import Comentario, Mensagem
from database import db

comentarios_bp = Blueprint('comentarios', __name__)

@comentarios_bp.route('/comentarios', methods=['POST'])
def criar_comentario():
    dados = request.json
    conteudo = dados.get('conteudo')
    mensagem_id = dados.get('mensagem_id')

    if not conteudo:
        return jsonify({"erro": "Conteúdo do comentário é obrigatório."}), 400

    mensagem = Mensagem.query.get(mensagem_id)
    if not mensagem:
        return jsonify({"erro": "Mensagem não encontrada."}), 404

    autor_id = 1  # autor padrão

    comentario = Comentario(conteudo=conteudo, mensagem_id=mensagem_id, autor_id=autor_id)
    db.session.add(comentario)
    db.session.commit()

    return jsonify({
        "id": comentario.id,
        "conteudo": comentario.conteudo,
        "dataHora": comentario.dataHora,
        "autor_id": comentario.autor_id,
        "mensagem_id": comentario.mensagem_id
    }), 201

@comentarios_bp.route('/mensagens/<int:mensagem_id>/comentarios', methods=['GET'])
def listar_comentarios_por_mensagem(mensagem_id):
    mensagem = Mensagem.query.get_or_404(mensagem_id)
    comentarios = Comentario.query.filter_by(mensagem_id=mensagem_id).all()
    return jsonify([{
        "id": c.id,
        "conteudo": c.conteudo,
        "dataHora": c.dataHora,
        "autor_id": c.autor_id,
        "mensagem_id": c.mensagem_id
    } for c in comentarios])

@comentarios_bp.route('/comentarios/<int:id>', methods=['PUT'])
def atualizar_comentario(id):
    comentario = Comentario.query.get_or_404(id)
    dados = request.json
    novo_conteudo = dados.get('conteudo')

    if not novo_conteudo:
        return jsonify({"erro": "Conteúdo do comentário não pode ser vazio."}), 400

    comentario.conteudo = novo_conteudo
    db.session.commit()

    return jsonify({
        "id": comentario.id,
        "conteudo": comentario.conteudo
    })

@comentarios_bp.route('/comentarios/<int:id>', methods=['DELETE'])
def deletar_comentario(id):
    comentario = Comentario.query.get_or_404(id)

    if comentario.autor_id != 1:  # só autor_id=1 pode excluir, por enquanto
        return jsonify({"erro": "Você não tem permissão para deletar este comentário."}), 403

    db.session.delete(comentario)
    db.session.commit()

    return jsonify({"mensagem": "Comentário deletado com sucesso."})
