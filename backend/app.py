from dotenv import load_dotenv
import os
from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman
from models.database import db

load_dotenv()

# =========================
# CONFIGURAÇÕES
# =========================
PORT = int(os.environ.get("PORT", 5000))
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# URL do frontend (Netlify) - Recomendado usar variável de ambiente
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://ancora-ecommerce.netlify.app")

# =========================
# APP
# =========================
app = Flask(__name__)

# =========================
# CORS (Único e bem configurado)
# =========================
CORS(app, resources={r"/*": {
    "origins": [
        FRONTEND_URL,
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    "supports_credentials": True,
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

# =========================
# TALISMAN (CSP corrigido para WebSocket)
# =========================
Talisman(
    app,
    content_security_policy={
        "default-src": "'self'",
        "connect-src": [
            "'self'",
            FRONTEND_URL,
            "https://*.onrender.com",   # Backend no Render
            "wss://*.onrender.com",     # WebSocket essencial
            "ws://*.onrender.com"
        ],
        "img-src": ["'self'", "data:", "blob:"],
        "script-src": ["'self'", "'unsafe-inline'"],
    },
    force_https=True,
    strict_transport_security=True
)

# =========================
# CONFIGURAÇÕES DA APLICAÇÃO
# =========================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'files')
app.config['MAX_CONTENT_LENGTH'] = 2048 * 1024 * 1024   # 2GB

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

# =========================
# SOCKETIO
# =========================
from routes.websocket import socketio

socketio.init_app(
    app,
    cors_allowed_origins=[FRONTEND_URL, "http://localhost:5173"],
    async_mode="eventlet",           # Melhor opção para Render
    logger=True,
    engineio_logger=True,
    ping_timeout=60,
    ping_interval=25
)

# =========================
# IMPORTS DOS BLUEPRINTS E WEBSOCKETS
# =========================
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

# Imports dos WebSockets (mantém como tinhas)
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

# =========================
# REGISTRO DOS BLUEPRINTS
# =========================
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
# app.register_blueprint(logout_bp)   # descomenta se estiveres a usar

# =========================
# DATABASE SETUP
# =========================
# =========================
# DATABASE SETUP
# =========================
def setup_database():
    with app.app_context():
        db.create_all()
        print("✅ Tabelas criadas com sucesso")


# =========================
# RUN (para Render usar Gunicorn)
# =========================
# if __name__ == '__main__':
 #   setup_database()
  #  print("=" * 70)
  #  print("🚀 SERVIDOR FLASK + SOCKETIO INICIADO")
  #  print(f"🌍 Porta: {PORT} | Debug: {DEBUG}")
  #  print(f"🌐 Frontend: {FRONTEND_URL}")
  #  print("=" * 70)

    # Apenas para rodar localmente
 #   socketio.run(
    #    app,
     #   host="0.0.0.0",
     #   port=PORT,
     #   debug=DEBUG,
      #  allow_unsafe_werkzeug=DEBUG
 #   )
    
