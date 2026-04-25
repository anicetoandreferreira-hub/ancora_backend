from flask import jsonify , Blueprint
from models.database import db, Amizade

# Rota para buscar notificações (pedidos de amizade pendentes)
notificacao = Blueprint("notificacao" , __name__)
@notificacao.route('/notificacoes/<int:usuario_id>', methods=['GET'])
def buscar_notificacoes(usuario_id):
    try:
        # 1. Busca na tabela Amizade todos os registros para este destinatário
        # que ainda não foram aceitos ou recusados
        pedidos_pendentes = Amizade.query.filter_by(
            destinatario_id=usuario_id, 
            status='pendente' 
           
        ).all()
        total_pedido = Amizade.query.filter_by(
            destinatario_id=usuario_id, 
            status='pendente',
            visualizada = False
        ).count()

        # 2. Transforma os dados em uma lista de dicionários (JSON)
        total = 0
        if total_pedido:
            total = total_pedido
            print(f"if-este é o dados do total de pedido:{total}")
        else:
            total = 0
            

        resultado = []
        for pedido in pedidos_pendentes:
            # O pedido.remetente vem do 'relationship' que criamos no Model
            resultado.append({
                "id_pedido": pedido.id,
                "de_id": pedido.remetente_id,
                "nome_remetente": pedido.remetente.nome,
                "mensagem": f"enviou um pedido de amizade!",
                "data": pedido.data_criacao.strftime('%d/%m/%Y %H:%M'),
                "total_notificacao":total
            })

        return jsonify(resultado), 200

    except Exception as e:
        print(f"Erro ao buscar notificações: {e}")
        return jsonify({"erro": "Erro interno no servidor"}), 500