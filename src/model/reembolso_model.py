from  src.model import db
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, DECIMAL, Date
from sqlalchemy import func

class Reembolso(db.model):  # <-- Interpreta que essa classe vai ser o modelo para a entidade
#---------------------------------------ATRIBUTOS---------------------------------------
    id = Column(Integer, primary_key=True, autoincrement=True)
    colaborador = Column(String(100), nullable=False)
    empresa = Column(String(50), nullable=False)
    num_prestacao = Column(Integer, nullable=False)
    descricao = Column(String(255))
    data = Column(Date, nullable=False, server_default=func.current_date())
    tipo_reembolso = Column(String(35), mullable=False)
    centro_custo = Column(String(50) nullable=False)
    ordem_interna = Column(String(50))
    divisao = Column(String(50))
    pep = Column(String(50))
    moeda = Column(String(20) nullable=False)
    distacia_km = Column(String(50))
    valor_km = Column(String(50))
    valor_faturado = Column(DECIMAL(10,2), nullable=False)  # <-- 999999999.22
    despesa = Column(DECIMAL(10,2))
    id_colaborador = Column(ForeignKey(column="colaborador.id"))
    status = Column(String(20), nullable=False)
    
#----------------------------------------------------------------------------------------
    def __init__(self, colaborador, empresa, num_prestacao, descricao, data, tipo_reembolso, centro_custo, ordem_interna, divisao, pep, moeda, distancia_km, valor_km, valor_faturado, despesa, id_colaborador, status='Em análise'):  #self liga o objeto ao atributo da classe
        self.colaborador = colaborador
        self.empresa = empresa
        self.num_prestacao = num_prestacao
        self.descricao = descricao
        self.data = data
        self.tipo_reembolso = tipo_reembolso
        self.centro_custo = centro_custo
        self.ordem_interna = ordem_interna
        self.divisao = divisao
        self.pep = pep
        self.moeda = moeda
        self.distacia_km = distancia_km
        self.valor_km = valor_km
        self.valor_faturado = valor_faturado
        self.despesa = despesa
        self.id_colaborador = id_colaborador
        self.status = status
        
    def all_data(self) -> dict:
        return {
            'colaborador': self.colaborador,
            'empresa': self.empresa,
            'num_prestacao': self.num_prestacao,
            'descricao': self.descricao,
            'data': self.data,
            'tipo_reembolso': self.tipo_reembolso,
            'centro_custo': self.centro_custo,
            'ordem_interna': self.ordem_interna,
            'divisao': self.divisao,
            'pep': self.pep,
            'moeda': self.moeda,
            'distancia_km': self.distancia_km,
            'valor_km': self.valor_km,
            'valor_faturado': self.valor_faturado,
            'despesa': self.despesa,
            'status': self.status
        }