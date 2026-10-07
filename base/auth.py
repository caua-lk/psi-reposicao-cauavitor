from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import database


auth_bp = Blueprint("auth", __name__)
@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        if nome and email and senha:
            hashed = generate_password_hash(senha)
            ifuser = database.buscar_usuario_por_email(email=email)
            if ifuser:
                return redirect(url_for("auth.login"))
            database.criar_usuario(nome=nome,email=email,senha_hash=hashed)
            return redirect(url_for('auth.login'))
        flash("Implemente o cadastro com hash de senha.")
        return redirect(url_for("auth.registro"))

    return render_template("registro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = database.buscar_usuario_por_email(email=email)
        if usuario:
            if check_password_hash(usuario.senha_hash, senha):
                session['usuario_id'] = usuario.id 
                session['usuario_nome'] = usuario.nome 
                flash
        return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    if "usuario_id" in session:
        session.clear()
        flash("saiu.")
        return redirect(url_for("index"))
    flash("Não há sessão.")
    return redirect(url_for('index'))
# Complete este arquivo durante a avaliação.
#
# O Blueprint já está criado, mas nenhuma rota foi vinculada ainda.
# Implemente aqui:
#
# - a rota /registro;
# - a rota /login;
# - a rota /logout.
