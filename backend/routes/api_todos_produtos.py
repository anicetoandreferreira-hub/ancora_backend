from flask import Blueprint , jsonify
from models.database import Registrar_produto

Todos_produtos = Blueprint("Todos_produtos" , __name__)

@Todos_produtos.route("/buscar_todos_produtos" , methods = ["GET"])
def buscar_todos_produtos ():
    try:
        todos_produtos = Registrar_produto.query.all()
        lista_produto = []
        for lista in todos_produtos:
                item = {
                    "nome_produto": lista.nome_produto,
                    "descricao_produto": lista.descricao_produto,
                    "tipo_produto": lista.tipo_produto,
                    "preco_produto": lista.preco_produto,
                    "url_imagem_produto": lista.url_imagem_produto,
                    "id_usuario": lista.id_usuario
                }
                lista_produto.append(item)
        return jsonify(lista_produto)
    except Exception as erro:
         print(f"erro ao buscar todos os produtos: {erro}")

    
