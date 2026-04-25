# routes/websocket.py
from flask_socketio import SocketIO

socketio = SocketIO(
    cors_allowed_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1"
    ],
    cookie='io',  # MUDOU: True -> 'io' ou remove a linha toda
    async_mode='threading',
    logger=True,
    engineio_logger=True
)