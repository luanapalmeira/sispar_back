#tarefa -> implementação

#Rota de visualização de todos os reembolsos -> GET 
#Solicitação de reembolsos -> POST

# Pra enviar múltiplos dados para o banco de dados, utilize: db.session.bulk_save_objects(lista[instancias])

#FAZER AS ROTAS RESPONDEREM NO POSTMAN! Como está na outra aba de controller

from flask import Blueprint, request, jsonify
from src.model.reembolso_model import Reembolso
from src.model import db

bp_reembolso = Blueprint('reembolso', __name__, url_prefix='/reembolso')


@bp_reembolso.route('/todos-reembolsos')
def visualizar_todos_reembolsos():
    reembolsos = db.session.execute(
        db.select(Reembolso)
    ).scalars().all()
    
    reembolsos = [reembolso.all_data() for reembolso in reembolsos]
    
    return jsonify(reembolsos), 200

@bp_reembolso.route('/solicitar-reembolso', methods=['POST'])
def solicitar_reembolsos():
    dados = request.get_json()

    reembolsos = []

    novo_reembolso = Reembolso(
        colaborador=dados['colaborador'],
        empresa=dados['empresa'],
        num_prestacao=dados['num_prestacao'],
        descricao=dados['descricao'],
        data=dados['data'],
        tipo_reembolso=dados['tipo_reembolso'],
        centro_custo=dados['centro_custo'],
        ordem_interna=dados['ordem_interna'],
        divisao=dados['divisao'],
        pep=dados['pep'],
        moeda=dados['moeda'],
        distancia_km=dados['distancia_km'],
        valor_km=dados['valor_km'],
        valor_faturado=dados['valor_faturado'],
        despesa=dados['despesa']
    )
    reembolsos.append(novo_reembolso)

    db.session.bulk_save_objects(reembolsos)
    db.session.commit()

    return jsonify({'mensagem': 'Reembolso cadastrado com sucesso'}), 201