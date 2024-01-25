# criar os formulários do site
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, ValidationError, FileField
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.validators import Email, EqualTo, Length, DataRequired
from fakepinterest.models import Usuario
from fakepinterest import bcrypt
import re


# def validar_email(self, campo):
#     email = campo.data
#     email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{1,3}$"
#     if not re.match(email_regex, email):
#         raise ValidationError('Email incorreto')


class FormLogin(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired(), Email()],
                       render_kw={'placeholder': 'Digite o e-mail'})
    senha = PasswordField('Senha', validators=[DataRequired()], render_kw={'placeholder': 'Digite a senha'})
    botao_confirmar = SubmitField('Fazer Login')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError('Email não encontrado. Crie uma conta')

    def validate_senha(self, senha):
        usuario = Usuario.query.filter_by(email=self.email.data).first()
        if not bcrypt.check_password_hash(usuario.senha, senha.data):
            raise ValidationError('Senha Incorreta!')


class FormCriarConta(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired(), Email()],
                       render_kw={'placeholder': 'Digite o e-mail'})
    username = StringField('Username', validators=[DataRequired()], render_kw={'placeholder': 'Digite o username'})
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)],
                          render_kw={'placeholder': 'Digite a senha'})
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')],
                                    render_kw={'placeholder': 'Digite a senha novamente'})
    botao_confirmar = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email cadastrado, faça o login')

    def validate_username(self, username):
        username_usuario = Usuario.query.filter_by(username=username.data).first()
        if username_usuario:
            raise ValidationError('Username já cadastrado. Informe outro')


class FormFoto(FlaskForm):
    foto = FileField('Foto', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Somente imagens!')])
    botao_confirmar = SubmitField('Enviar')
