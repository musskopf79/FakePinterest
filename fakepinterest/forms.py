# Criar os formulários do site
#pip install flask-wtf email_validator

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fakepinterest.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_entrar = SubmitField("Fazer login")

class FormCriarConta(FlaskForm):
    username = StringField("Nome de usuário", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6,20)])
    confirmacao_senha = PasswordField("Confirmação de senha", validators=[DataRequired(), EqualTo("senha")])
    botao_criar = SubmitField("Criar conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        #filter_by porque estamos procurando se existe um e-mail igual (=! de filter_get)
        #email = resultado da query do Usuário no banco de dados (importado)
        #email.data = campo de e-mail do formulário
        if usuario:
            return ValidationError("E-mail já cadastrado, faça login para continuar")

class FormPost(FlaskForm):
    post = FileField("Post", validators=[DataRequired()])
    botao_enviar = SubmitField("Postar foto")