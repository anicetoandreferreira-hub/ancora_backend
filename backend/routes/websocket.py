from flask_socketio import SocketIO

socketio = SocketIO(
    cors_allowed_origins=[
        "https://ancora-ecommerce.netlify.app"
    ],
    async_mode="eventlet",
    logger=True,
    engineio_logger=True,
    manage_session=False
)
