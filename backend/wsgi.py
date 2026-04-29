# wsgi.py   ← Este é o mais importante
import eventlet
eventlet.monkey_patch()   # ← Tem que ser a PRIMEIRA coisa a ser executada

from app import app, socketio

# Para rodar localmente (opcional)
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)
