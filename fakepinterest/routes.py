# criar as rotas (links) do site
from flask import render_template, url_for, redirect, abort
from fakepinterest.models import Usuario, Foto
from fakepinterest import app, bcrypt, database
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
from werkzeug.utils import secure_filename
import os


@app.route('/', methods=['GET', 'POST'])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        senha = formlogin.senha.data
        if usuario and bcrypt.check_password_hash(usuario.senha.encode('utf-8'), senha):
            login_user(usuario, remember=True)
            return redirect(url_for('perfil', id_usuario=usuario.id))
    return render_template('homepage.html', form=formlogin)


@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
    form_criar_conta = FormCriarConta()
    if form_criar_conta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criar_conta.senha.data).decode('utf-8')
        usuario = Usuario(username=form_criar_conta.username.data,
                          senha=senha,
                          email=form_criar_conta.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for('perfil', id_usuario=usuario.id))
    return render_template('criarconta.html', form=form_criar_conta)


@app.route('/perfil/<id_usuario>', methods=['GET', 'POST'])
@login_required
def perfil(id_usuario):
    # verificiar se o perfil que a pessoa está visualizando é dela mesmo
    if int(id_usuario) == int(current_user.id):
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            caminho_padrao = os.path.abspath(os.path.dirname(__file__))
            caminho_salvar = os.path.join(caminho_padrao, app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho_salvar)
            # salvar a foto no banco de dados
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()

        return render_template('perfil.html', usuario=current_user, form=form_foto)

    else:
        usuario = Usuario.query.get(int(id_usuario))
        if usuario:
            return render_template('perfil.html', usuario=usuario, form=None)
        else:
            abort(404)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/feed')
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template('feed.html', fotos=fotos)