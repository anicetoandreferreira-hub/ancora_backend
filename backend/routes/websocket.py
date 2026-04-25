from flask_socketio import SocketIO

socketio = SocketIO(
    cors_allowed_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://ancora-ecommerce.netlify.app/"
    ],
    async_mode="eventlet",
    logger=True,
    engineio_logger=True,
    ping_timeout=60,
    ping_interval=25,
    allow_upgrades=True
)
