import pytest
from src.app import create_app
from src.model.colaborador_model import Colaborador
import time 

#---------------------------------CONFIGURAÇÕES---------------------------------
@pytest.fixture  #Configura os testes
def app():
    app = create_app()
    yield app  #yield -> vai armazenar o valor em memória. O que a linha faz: yield vai transformar a váriavel dentro de uma função de algo em escopo local para em escopo global.
    
@pytest.fixture  #Configura nossos teste de requisição
def client(app):
    return app.test_client()
#-------------------------------------------------------------------------------

def test_pegar_todos_colaboradores(client):
    
    resposta = client.get('/colaborador/todos-colaboradores')
    
    #assert -> Vai dizer se os nossos testes estão sendo concluídos ou não
    assert resposta.status_code == 200
    assert isinstance(resposta.json, list)
    
#Teste de eficiência de desempenho
def test_desempenho_requisicao_get(client):
    
    comeco = time.time()  #Pega a hora atual e tranforma ela em segundos
    
    for _ in range(100): # _ = Omite a variável auxiliar
        resposta = client.get('/colaborador/todos-colaboradores')
        
    fim = time.time() - comeco
    
    assert fim < 0.5 #Indica os segundos