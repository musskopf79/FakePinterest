# Criar as rotas do nosso site (links / páginas.html)

from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormPost
from fakepinterest.models import Usuario, Postagem
import os
from werkzeug.utils import secure_filename

@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id_usuario))
    return render_template("homepage.html", formulario=form_login)
    #O campo 'formulario' é o nome para a página .html
    # O campo 'formlogin' é a variável (não a função!). Fica em minúsculo.

@app.route("/criar_conta", methods=["GET", "POST"])
def criar_conta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data,
                          email=form_criarconta.email.data,
                          senha=senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id_usuario) )
    return render_template("criar_conta.html", formulario=form_criarconta)
    #Os 2 campos 'formulario' tem o mesmo nome, para que a página homepage possa ser igual (uma cópia) da página criarconta
    # O campo 'form_criarconta' é a variável (não a função!). Fica em minúsculo.

@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id_usuario):
        # Usuário está vendo seu próprio perfil.
        form_post = FormPost()
        if form_post.validate_on_submit():
            arquivo = form_post.post.data
            # precisa corrigir o nome para não ter caracteres especiais, por exemplo
            nome_corrigido = secure_filename(arquivo.filename)
            # salvar o arquivo no fotos_post
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              #estamos pegando o caminho absoluto de onde está o arquivo (__file__) em uso (routes.py)
                              app.config["UPLOAD_FOLDER"], nome_corrigido)
            arquivo.save(caminho)
            # registrar o nome no banco de dados
            postagem = Postagem(imagem=nome_corrigido, id_usuario=current_user.id_usuario)
            database.session.add(postagem)
            database.session.commit()

        return render_template("perfil.html", usuario=current_user, form=form_post)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/feed")
def feed():
    fotos = Postagem.query.order_by(Postagem.data_criacao).all()
    return render_template("feed.html", fotos=fotos)