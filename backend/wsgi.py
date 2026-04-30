# wsgi.py
import gevent.monkey
gevent.monkey.patch_all()   # Deve ser a primeira coisa a ser executada

from app import app

# Para rodar localmente (opcional)
if __name__ == "__main__":
    from app import socketio
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)
