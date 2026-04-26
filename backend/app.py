from dotenv import load_dotenv
import os

# 🔥 IMPORTANTE: monkey patch antes de tudo
import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_cors import CORS
from models.database import db
from flask_talisman import Talisman

load_dotenv()

PORT = int(os.environ.get("PORT", 5000))
DEBUG = os.environ.get("DEBUG", "False") == "True"
REDIS_URL = os.getenv("REDIS_URL")  # ex: rediss://...upstash.io

from routes.websocket import socketio

# ... teus imports de rotas iguais ...

app = Flask(__name__)

# CORS
CORS(app, resources={r"/*": {
    "origins": [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://ancora-ecommerce.netlify.app"
    ],
    "supports_credentials": True
}})

# Talisman - corrige CSP
BACKEND_URL = os.getenv("RENDER_EXTERNAL_URL", "")  # Render injeta isto
Talisman(
    app,
    content_security_policy={
        "default-src": "'self'",
        "connect-src": [
            "'self'",
            "https://ancora-ecommerce.netlify.app",
            "wss://*.onrender.com",  # permite o teu backend
            "https://*.onrender.com"
        ],
        "img-src": ["'self'", "data:", "blob:", "https:"]
    },
    force_https=False,  # Render já faz SSL
    strict_transport_security=False
)

# DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'files')
app.config['MAX_CONTENT_LENGTH'] = 2048 * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db.init_app(app)

# 🔥 SOCKET COM REDIS
socketio.init_app(
    app,
    cors_allowed_origins=[
        "https://ancora-ecommerce.netlify.app",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    async_mode="eventlet",          # em vez de threading
    message_queue=REDIS_URL,        # <-- Redis aqui
    ping_interval=25,               # keepalive para Render não matar
    ping_timeout=60,
    logger=True,
    engineio_logger=DEBUG
)

def setup_database():
    with app.app_context():
        db.create_all()
        print("✅ Tabelas criadas")

# blueprints iguais...

if __name__ == '__main__':
    setup_database()
    socketio.run(app, host="0.0.0.0", port=PORT, debug=DEBUG)
