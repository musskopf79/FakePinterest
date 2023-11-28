# Criar estrutura do banco de dados
from fakepinterest import database
from datetime import datetime

class Usuario(database.Model):
    id_usuario = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable = False, unique=True)
    email = database.Column(database.String, nullable = False, unique=True)
    senha = database.Column(database.String, nullable = False)
    fotos = database.relationship("Postagem", backref="usuario", lazy=True)

class Postagem(database.Model):
    id_post = database.Column(database.Integer, primary_key=True)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id_usuario'), nullable = False)
    imagem = database.Column(database.String, default="default.png")
    data_criacao = database.Column(database.DateTime, nullable = False, default=datetime.utcnow())
