# app.py
from dotenv import load_dotenv
import os
from flask import Flask
from flask_cors import CORS
from models.database import db
from flask_talisman import Talisman
load_dotenv()

# 🔥 ADICIONADO (lógica de deploy)
PORT = int(os.environ.get("PORT", 5000))
DEBUG = os.environ.get("DEBUG", "True") == "True"

# Importa o socketio DEPOIS do load_dotenv
from routes.websocket import socketio

from routes.api_register import registrar
from routes.api_auth import login_bp
from routes.api_usuario import users_bp
from routes.api_get_date_perfil import date_perfil_user
from routes.websocket_notificacao import notificacao
from routes.api_nitificacao_visualizada import notificacao_visualizada
from routes.api_meus_amigos import meus_amigos
from routes.api_get_quantidade_menssagem import quantidade_menssagem
from routes.api_registrar_produto import registrar_produto
from routes.api_buscar_produtos_usuario import buscar_produto_Usuario
from routes.api_upload_file import upload_bp
from routes.api_todos_produtos import Todos_produtos
from routes.api_me import login_bp as me_bp
from routes.api_logout import login_bp as logout_bp


# Imports dos websockets
import routes.websoket_conectUser
import routes.websocket_aceitar_pedido_amizade
import routes.websocket_recusar_pedido_amizade 
import routes.websocket_entrar_na_sala
import routes.websocket_enviar_menssagem
import routes.websocket_usuario_digitando
import routes.websocket_buscar_menssagens
import routes.websocket_sair_da_sala
import routes.websoket_menssagem_visualizada
import routes.websocket_nova_quantidade_de_menssagem
import routes.websocket_Eliminar_menssagem
import routes.websocket_Editar_menssagem

app = Flask(__name__)

CORS(app, resources={r"/*": {
    "origins": [
        "http://127.0.0.1:5173",
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5000"
    ],
    "supports_credentials": True,
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

# Headers de segurança
Talisman(app, 
    content_security_policy={
        'default-src': "'self'",
        'connect-src': ["'self'", "ws://127.0.0.1:5000", "http://127.0.0.1:5000"],
        'img-src': ["'self'", "data:", "blob:"],
    },
    force_https=False,  # True em prod
    strict_transport_security=False  # True em prod com HTTPS
)

# ... resto do app.py igual

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'files')
app.config['MAX_CONTENT_LENGTH'] = 2048 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

# REMOVIDO allow_unsafe_werkzeug daqui
socketio.init_app(app)

def setup_database():
    with app.app_context():
        db.create_all()
        print("✅ Tabelas criadas com sucesso")

app.register_blueprint(registrar)
app.register_blueprint(users_bp)
app.register_blueprint(date_perfil_user)
app.register_blueprint(notificacao)
app.register_blueprint(notificacao_visualizada)
app.register_blueprint(meus_amigos)
app.register_blueprint(quantidade_menssagem)
app.register_blueprint(registrar_produto)
app.register_blueprint(buscar_produto_Usuario)
app.register_blueprint(upload_bp)
app.register_blueprint(Todos_produtos)
app.register_blueprint(me_bp)


if __name__ == '__main__':
    setup_database()
    
    print("=" * 70)
    print("🚀 Servidor Flask + SocketIO iniciado com sucesso!")
    print("🌐 Acessível via rede em:")
    print(f"   • http://127.0.0.1:5000")
    print(f"   • http://10.184.55.66:5000")
    print(f"🌍 Porta dinâmica (deploy): {PORT}")  # 🔥 ADICIONADO
    print("=" * 70)

    socketio.run(
        app, 
        host="0.0.0.0", 
        port=PORT,  # 🔥 ALTERAÇÃO SEGURA (dinâmico)
        debug=DEBUG,  # 🔥 ADICIONADO (controlado por env)
        allow_unsafe_werkzeug=True  # SÓ AQUI, não no init_app
    )
