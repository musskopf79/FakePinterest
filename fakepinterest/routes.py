# Criar as rotas do nosso site (links / páginas.html)

from flask import render_template, url_for
from fakepinterest import app
from flask_login import login_required
from fakepinterest.forms import FormLogin, FormCriarConta

@app.route("/", methods=["GET", "POST"])
def homepage():
    formlogin = FormLogin()
    return render_template("homepage.html", formulario=formlogin)
    #O campo 'formulario' é o nome para a página .html
    # O campo 'formlogin' é a variável (não a função!). Fica em minúsculo.

@app.route("/criar_conta", methods=["GET", "POST"])
def criar_conta():
    formcriarconta = FormCriarConta()
    return render_template("criar_conta.html", formulario=formcriarconta)
    #Os 2 campos 'formulario' tem o mesmo nome, para que a página homepage possa ser igual (uma cópia) da página criarconta
    # O campo 'formcriarconta' é a variável (não a função!). Fica em minúsculo.

@app.route("/perfil/<usuario>")
@login_required
def perfil(usuario):
    return render_template("perfil.html", usuario=usuario)