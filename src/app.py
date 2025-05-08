# RESPONSÁVEL PELA CRIAÇÃO DA APLICAÇÃO
# CREATE_APP() -> VAI CONFIGURAR A INSTÂNCIA DO FLASK

from flask import Flask
from src.controller.colaborador_controller import bp_colaborador
from src.controller.reembolso_controller import bp_reembolso
from src.model import db
from config import Config
from flask_cors import CORS
from flasgger import Swagger

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",  # <-- Da um nome de referência para a documentação
            "route": "/apispec.json/",  # <-- Vai definir a rota do arquivo JSON para a construção da documentação
            "rule_filter": lambda rule: True,  # <-- Todas as rotas/endpoints serão documentadas
            "model_filter": lambda tag: True,  # <-- Especifica quais modelos da entidade serão documentados
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

def create_app():
    app = Flask(__name__)  # <---- instância do Flask 
    
    CORS(app, origins="*") # <----- A política de CORS seja implementada em TODA A APLICAÇÃO | Não colocar o * em origins por questões de insegurança, má prática.
    
    app.register_blueprint(bp_colaborador)
    
    app.register_blueprint(bp_reembolso)
    
    app.config.from_object(Config)
    
    db.init_app(app)  #Essa linha inicia a conexão com o banco de dados
    
    Swagger(app, config=swagger_config)
    
    with app.app_context():  #Se as tabelas não existem, crie.
        db.create_all()
    
    return app