# gunicorn_config.py  (versão simplificada)
import os

bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"
timeout = 120
loglevel = "info"
