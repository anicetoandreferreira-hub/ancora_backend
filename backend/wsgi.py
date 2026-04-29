# wsgi.py  ← Este será o arquivo principal para o Render

import eventlet
eventlet.monkey_patch()   # ← TEM que ser a PRIMEIRA coisa

from app import app, socketio   # Agora importamos o app depois do patch

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)
