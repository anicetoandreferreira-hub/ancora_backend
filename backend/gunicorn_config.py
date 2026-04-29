# gunicorn_config.py
import os

bind = "0.0.0.0:" + os.environ.get("PORT", "10000")
workers = 1
worker_class = "eventlet"
loglevel = "info"
timeout = 120
keepalive = 60
