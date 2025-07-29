from datetime import datetime
from database import db
import re

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    perfil = db.Column(db.String(10), default='USER')  # Pode ser USER ou ADMIN
    mensagens = db.relationship('Mensagem', backref='autor', lazy=True)

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    dataHora = db.Column(db.DateTime, default=datetime.utcnow)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    mensagem_id = db.Column(db.Integer, db.ForeignKey('mensagem.id'), nullable=False)

    autor = db.relationship('Usuario', backref='comentarios')
    mensagem = db.relationship('Mensagem', backref='comentarios')
