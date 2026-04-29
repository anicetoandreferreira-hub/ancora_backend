# wsgi.py
import eventlet
eventlet.monkey_patch()   # ← Obrigatório ser a primeira linha

from app import app       # Importamos apenas o 'app' (Flask)

if __name__ == "__main__":
    # Apenas para testes locais
    from app import socketio
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)
