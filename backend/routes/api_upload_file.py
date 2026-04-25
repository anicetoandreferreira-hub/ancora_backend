# routes/upload.py
from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
import uuid

# Cria o Blueprint (podes mudar o nome se quiseres)
upload_bp = Blueprint('upload', __name__, url_prefix='/api')

@upload_bp.route('/upload-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "Nenhum arquivo enviado"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"success": False, "error": "Nome do arquivo vazio"}), 400

    # Gera nome único seguro
    ext = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
    unique_filename = f"{uuid.uuid4()}.{ext}" if ext else str(uuid.uuid4())

    filename = secure_filename(unique_filename)

    # Usa o UPLOAD_FOLDER que vais definir no app principal
    upload_folder = current_app.config.get('UPLOAD_FOLDER')
    if not upload_folder:
        return jsonify({"success": False, "error": "Pasta de upload não configurada"}), 500

    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    return jsonify({
        "success": True,
        "file_path": f"/static/files/{filename}",
        "filename": file.filename,           # nome original que o utilizador enviou
        "size": os.path.getsize(file_path)
    })