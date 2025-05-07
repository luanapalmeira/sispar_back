from flask import Blueprint, request, jsonify
from src.model.colaborador_model import Colaborador
from src.model import db
from src.security.security import hash_senha, checar_senha
from flasgger import swag_from

#request -> um recurso do Flask que vai facilitar a captura dos dados na requisição. Trabalhar com requisições.
#jsonify -> envia os dados na requisição. Trabalha com as respostas. Vai utilizar ele no retorno. Responsável por serializar os dados (transformar aqueles dados em resposta no formato json)

bp_colaborador = Blueprint('colaborador', __name__, url_prefix='/colaborador') 


@bp_colaborador.route('/todos-colaboradores')
@swag_from('../docs/colaborador/todos_colaboradores_colaborador.yml')
def pegar_dados_todos_colaboradores():
    
    #Fazendo o acesso ao banco de dados
    colaboradores = db.session.execute(
        db.select(Colaborador)
    ).scalars().all()  #saclars() -> vai trazer vários dados ou um none. usa o all() para confirmar de trazer realmente todos os dados.

#     Execute essa expressão para cada item que você encontrar nesse iterável.
#                        Expressão                Item           Iterável
    colaboradores = [colaborador.all_data() for colaborador in colaboradores]
    
    Colaborador.query.filter_by(deletado=False).all()
    
    return jsonify(colaboradores), 200

@bp_colaborador.route('/cadastrar', methods=['POST']) 
@swag_from('../docs/colaborador/cadastrar_colaborador.yml')
def cadastrar_novo_colaborador():
    dados_requisicao = request.get_json()
    
    novo_colaborador = Colaborador(
        nome=dados_requisicao['nome'],  #Pegue do json o valor relacionado a chave nome
        email=dados_requisicao['email'],
        senha=hash_senha(dados_requisicao['senha']),
        cargo=dados_requisicao['cargo'],
        salario=dados_requisicao['salario']
    )
    
#   INSERT INTO tb_colaborador (nome, email, senha, cargo, salario) VALUES (VALOR1,VALOR2,VALOR3,VALOR4,VALOR5)
    db.session.add(novo_colaborador)
    db.session.commit()  #Essa linha executa a query
    
    return jsonify( {'mensagem': 'Colaborador cadastrado com sucesso'} ), 201  #status de created

#Sinaliza dados enviados
#endereco/colaborador/atualizar/2
@bp_colaborador.route('/atualizar/<int:id_colaborador>', methods=['PUT'])
@swag_from('../docs/colaborador/atualizar_colaborador.yml')
def atualizar_dados_colaborador(id_colaborador):
    dados_requisicao = request.get_json()

    colaborador = db.session.get(Colaborador, id_colaborador)

    if not colaborador:
        return jsonify({'mensagem': 'Colaborador não encontrado'}), 404

    if 'nome' in dados_requisicao:
        colaborador.nome = dados_requisicao['nome']
        
    if 'cargo' in dados_requisicao:
        colaborador.cargo = dados_requisicao['cargo']
        
    if 'salario' in dados_requisicao:
        colaborador.salario = dados_requisicao['salario']
        
    if 'email' in dados_requisicao:
        colaborador.email = dados_requisicao['email']
    
    if 'senha' in dados_requisicao:
        colaborador.senha = hash_senha(dados_requisicao['senha'])

    db.session.commit()  # <-- salva as alterações no banco

    return jsonify({'mensagem': 'Dados do colaborador atualizados com sucesso'}), 200

@bp_colaborador.route('/deletar/<int:id_colaborador>', methods=['DELETE'])
def deletar_colaborador(id_colaborador):
    colaborador = db.session.get(Colaborador, id_colaborador)

    if not colaborador:
        return jsonify({'erro': 'Colaborador não encontrado'}), 404

    #Soft delete: marca como deletado sem remover do banco
    colaborador.deletado = True
    db.session.commit()

    return jsonify({'mensagem': 'Colaborador marcado como deletado com sucesso'}), 200

@bp_colaborador.route('/restaurar/<int:id_colaborador>', methods=['PUT'])
def restaurar_colaborador(id_colaborador):
    colaborador = db.session.get(Colaborador, id_colaborador)

    if not colaborador:
        return jsonify({'erro': 'Colaborador não encontrado'}), 404

    if not colaborador.deletado:
        return jsonify({'mensagem': 'Colaborador já está ativo'}), 200

    colaborador.deletado = False
    db.session.commit()

    return jsonify({'mensagem': 'Colaborador restaurado com sucesso'}), 200

#Criando a regra de negócio para fazer o Login
@bp_colaborador.route('/login', methods=['POST'])
@swag_from('../docs/colaborador/login_colaborador.yml')
def login():
    dados_requisicao = request.get_json()
    
    email = dados_requisicao.get('email')
    senha = dados_requisicao.get('senha')
    
    #Fazendo as verificações
    if not email or not senha:
        return jsonify({'mensagem': 'Todos os dados precisam ser preenchidos'}), 400  # Bad request = erro por parte do cliente
    
    #Como se estivesse usando o comando -> SELECT * FROM [TABELA]
    #Query
    colaborador = db.session.execute(
        db.select(Colaborador).where(Colaborador.email == email)  #Se fizer um select sem where, irá trazer todas as informações que estão na tabela para o nosso servidor
    ).scalar() #Um método especial do ORM que vai trazer apenas um registro ou ele vai deixar a variável Colaborador como none (vai trazer a linha de informação OU None)
    
    print('*'*100)
    print(f'dado: {colaborador} é do tipo {type(colaborador)}')
    print('*'*100)
    
    #Se o colaborador não tiver nenhum valor
    if not colaborador:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    
    colaborador = colaborador.to_dict()
    
    print('*'*100)
    print(f'dado: {colaborador} é do tipo {type(colaborador)}')
    print('*'*100)
    
    if email == colaborador.get('email') and checar_senha(senha, colaborador.get('senha')):
        return jsonify({'mensagem': 'Login realizado com sucessso'}), 200
    else:
        return jsonify({'mensagem': 'Credenciais inválidas'}), 400
    