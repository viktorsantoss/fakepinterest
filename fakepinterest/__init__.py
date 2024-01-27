from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)

if os.getenv('DEBUG') == '0':
    link_banco = os.getenv('DATABASE_URL')
    senha = os.getenv('SENHA_SECRETA')
else:
    link_banco = "sqlite:///comunidade.db"
    senha = '888b4eff900cfc5f7c711d4f90b382cc'

app.config["SQLALCHEMY_DATABASE_URI"] = link_banco
app.config["SECRET_KEY"] = senha
app.config['UPLOAD_FOLDER'] = 'static/fotos_posts'

login = LoginManager(app)
# definir a página para qual o usuário vai ser direcionada caso não tenha autenticação
login.login_view = 'homepage'

bcrypt = Bcrypt(app)

database = SQLAlchemy(app)


from fakepinterest import routes
