socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode="eventlet",
    logger=True,
    engineio_logger=True
)
