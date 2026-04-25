from flask import Blueprint , request , json , jsonify
from service.api_register import register_user
registrar = Blueprint("registrar" , __name__)

@registrar.route("/api/Registrar" , methods=["post"])
def registro():
    dados = request.get_json()
    nome = dados.get("nome")
    telefone = dados.get("telefone")
    senha = dados.get("senha")
    confirmar_senha = dados.get("confirmar_senha")

    serviço = register_user()
    resultado = serviço.registrar_usuario(nome,telefone,senha,confirmar_senha)

    return jsonify({"status": resultado})
