# Criar estrutura do banco de dados


from fakepinterest import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    #get, pois queremos o usuário específico, pelo ID (!= de filter_by)
    return Usuario.query.get(int(id_usuario))    

class Usuario(database.Model, UserMixin):
    id_usuario = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable = False, unique=True)
    email = database.Column(database.String, nullable = False, unique=True)
    senha = database.Column(database.String, nullable = False)
    fotos = database.relationship("Postagem", backref="usuario", lazy=True)

    def get_id(self):
        return self.id_usuario
    # Como não estou usando a chave como "id" (e sim id_usuário), precisa definir a opção get_id, pois é usada em vários comandos do flask-login

    
class Postagem(database.Model):
    id_post = database.Column(database.Integer, primary_key=True)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id_usuario'), nullable = False)
    imagem = database.Column(database.String, default="default.png")
    data_criacao = database.Column(database.DateTime, nullable = False, default=datetime.utcnow())
