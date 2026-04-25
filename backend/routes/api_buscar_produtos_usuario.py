from flask import Blueprint, jsonify
from models.database import Registrar_produto

buscar_produto_Usuario = Blueprint("buscar_produto_Usuario", __name__)

@buscar_produto_Usuario.route("/buscar_produto_usuario/<int:id_usuario>", methods=["GET"])
def buscar_produto_ususuario(id_usuario):
    try:
        # Busca todos os produtos filtrados pelo ID do usuário
        produtos = Registrar_produto.query.filter_by(id_usuario=id_usuario).all()

        if not produtos:
            return jsonify([]), 200 # Retorna lista vazia se não achar nada

        array_lista = []
        
        for p in produtos:
            # Criamos UM dicionário para CADA produto
            item = {
                "nome_produto": p.nome_produto,
                "descricao_produto": p.descricao_produto,
                "tipo_produto": p.tipo_produto,
                "preco_produto": p.preco_produto,
                "url_imagem_produto": p.url_imagem_produto,
                "id_usuario": p.id_usuario
            }
            array_lista.append(item)

        return jsonify(array_lista), 200

    except Exception as erro:
        print(f"Erro ao buscar os produtos do usuario: {erro}")
        # Lembre-se do str(erro) para o JSON não quebrar!
        return jsonify({"status": "erro", "detalhes": str(erro)}), 500