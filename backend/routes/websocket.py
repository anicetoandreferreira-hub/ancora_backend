from flask_socketio import SocketIO

socketio = SocketIO(
    cors_allowed_origins=[
        "http://localhost:5173",
        "https://ancora-ecommerce.netlify.app"
    ],
    async_mode="threading",  # 🔥 IMPORTANTE
    logger=True,
    engineio_logger=True
)
