#tarefa -> implementação

#Rota de visualização de todos os reembolsos -> GET 
#Solicitação de reembolsos -> POST

# Pra enviar múltiplos dados para o banco de dados, utilize: db.session.bulk_save_objects(lista[instancias])

#FAZER AS ROTAS RESPONDEREM NO POSTMAN! Como está na outra aba de controller

from flask import Blueprint, request, jsonify
from src.model.reembolso_model import Reembolso
from src.model import db
from datetime import datetime
from flasgger import swag_from

bp_reembolso = Blueprint('reembolso', __name__, url_prefix='/reembolso')


@bp_reembolso.route('/todos-reembolsos')
@swag_from('../docs/reembolso/todos_reembolsos_reembolso.yml')
def visualizar_todos_reembolsos():
    reembolsos = db.session.execute(
        db.select(Reembolso)
    ).scalars().all()
    
    reembolsos = [reembolso.all_data() for reembolso in reembolsos]

    
    return jsonify(reembolsos), 200

@bp_reembolso.route('/solicitar-reembolso', methods=['POST'])
@swag_from('../docs/reembolso/solicitar_reembolso_reembolso.yml')
def solicitar_reembolsos():
    dados = request.get_json()
    
    data_editada = datetime.strptime(dados.get('data'), '%d/%m/%Y').date()
    
    reembolsos = []

    novo_reembolso = Reembolso(
        colaborador=dados['colaborador'],
        empresa=dados['empresa'],
        num_prestacao=dados['num_prestacao'],
        descricao=dados['descricao'],
        data=data_editada,
        tipo_reembolso=dados['tipo_reembolso'],
        centro_custo=dados['centro_custo'],
        ordem_interna=dados.get('ordem_interna'),
        divisao=dados.get('divisao'),
        pep=dados.get('pep'),
        moeda=dados['moeda'],
        distancia_km=dados.get('distancia_km'),
        valor_km=dados.get('valor_km'),
        valor_faturado=dados['valor_faturado'],
        despesa=dados.get('despesa'),
        id_colaborador=dados.get('id_colaborador'),
        status=dados.get('status', 'Em análise')
    )
    reembolsos.append(novo_reembolso)

    db.session.bulk_save_objects(reembolsos)
    db.session.commit()

    return jsonify({'mensagem': 'Reembolso cadastrado com sucesso'}), 201

@bp_reembolso.route('/reembolso/<num_prestacao>')
@swag_from('../docs/reembolso/reembolso_prestacao_reembolso.yml')
def visualizar_reembolso_por_prestacao(num_prestacao):
    reembolso = db.session.execute(
        db.select(Reembolso).filter_by(num_prestacao=num_prestacao)
    ).scalars().first()

    if not reembolso:
        return jsonify({'mensagem': 'Reembolso não encontrado'}), 404

    return jsonify(reembolso.all_data()), 200