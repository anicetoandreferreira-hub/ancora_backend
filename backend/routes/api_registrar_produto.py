from flask import Blueprint, jsonify, request
from models.database import Registrar_produto, db
from routes.websocket import socketio
import os


registrar_produto = Blueprint("registrar_produto", __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')


@registrar_produto.route("/registrar_produto", methods=["POST"])
def registrarProduto():
    try:
        imagem = request.files.get("imagem_produto")
        nome_produto = request.form.get("nome_produto")
        descricao_produto = request.form.get("descricao_produto")
        tipo_produto = request.form.get("tipo_produto")
        preco_produto = request.form.get("preco_produto")
        id_usuario = request.form.get("id_usuario")

        if not imagem or imagem.filename == '':
            return jsonify({"status": "Erro: Nenhuma imagem selecionada!"}), 400

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        nome_imagem = f"ancora_{imagem.filename.replace(' ', '_')}"
        rota_completa = os.path.join(UPLOAD_FOLDER, nome_imagem)
        
        imagem.save(rota_completa)

        url_para_banco = f"/static/uploads/{nome_imagem}"

        print(f"Imagem salva em: {rota_completa}")

        # Registrar no banco
        dados = {
            "nome_produto": nome_produto,
            "descricao_produto": descricao_produto,
            "tipo_produto": tipo_produto,
            "preco_produto": preco_produto,
            "url_imagem_produto": url_para_banco,
            "id_usuario": id_usuario
        }
        novo_produto = Registrar_produto(**dados)
        db.session.add(novo_produto)
        db.session.commit()

        # ====================== EMIT CORRIGIDO (sem broadcast) ======================
        produto_data = {
            "id": novo_produto.id,
            "nome": novo_produto.nome_produto,
            "descricao": novo_produto.descricao_produto,
            "tipo": novo_produto.tipo_produto,
            "preco": novo_produto.preco_produto,
            "url_imagem_produto": novo_produto.url_imagem_produto,
            "id_usuario": novo_produto.id_usuario,
            "data_registro": str(getattr(novo_produto, 'data_registro', None))
        }

        # Forma correta e compatível com todas as versões recentes:
        socketio.emit("produto_registrado", produto_data, namespace="/")

        print(f"✅ Produto emitido via socket: {novo_produto.nome_produto}")
        # ===========================================================================

        return jsonify({
            "status": "produto registrado com sucesso!", 
            "url": url_para_banco,
            "produto": produto_data
        })
    
    except Exception as erro:
        print(f"Erro ao registrar o produto: {erro}")
        db.session.rollback()
        return jsonify({"status": str(erro)}), 500