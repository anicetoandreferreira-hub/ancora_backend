
# wsgi.py
import gevent.monkey
gevent.monkey.patch_all()     # ← Substitui o eventlet.monkey_patch

from app import app

if __name__ == "__main__":
    from app import socketio
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)
