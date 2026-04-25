from flask_socketio import SocketIO

socketio = SocketIO(
    cors_allowed_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://ancora-oficial-ao.netlify.app",
        "https://ancora-oficial-ao.netlify.app/"
    ],
    async_mode="eventlet",
    logger=True,
    engineio_logger=True
)
