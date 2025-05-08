#Armazenar as configurações do ambiente de desenvolvimento
#ORM - Mapeamento Objeto-Relacional. É uma ponte entre o banco de dados e o código (entende os dois lados e cuida dessa comunicação)

from os import environ   #Esse arquivo tem acesso as varíaveis de ambiente
from dotenv import load_dotenv   #Permite o carregamento das variáveis de ambiente nesse arquivo

load_dotenv()

class Config():  #Por padrão, o nome das classes precisam estar em Pascal Case (Primeira letra maiúscula)
    SQLALCHEMY_DATABASE_URI = environ.get('URL_DATABASE_PROD')  #Puxa a variável de ambiente e utiliza para a conexão do ORM ao banco de dados
    SQLALCHEMY_TRACK_MODIFICATIONS = False  #Otimizando as querys no banco de dados