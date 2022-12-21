from cesta import Cesta
from familia import Familia
from alimento import Alimento
from tipoAlimento import TipoAlimento
from entrega import Entrega
from datetime import date, time

class CestaAction:

    def __init__(self, id, data = 0, name = 0, peso = 0):
        self.id = id
        self.data = data
        self.name = name
        self.peso = peso
    
    @staticmethod
    def loadData():
        cestas = Cesta.loadAllEntities()
        cdata = []
        for cesta in cestas:
            action = CestaAction.loadInfo(cesta)
            cdata.append(action)
        
        return cdata
    
    @staticmethod
    def loadDataForId(id):
        cesta = Cesta.loadFromId(id)
        return CestaAction.loadInfo(cesta)

    @staticmethod
    def loadDetailsForCesta(id):
        alimentos = Alimento.loadAllEntitiesForCesta(id)
        details = []
        for alimento in alimentos:
            tipo = TipoAlimento.loadFromId(alimento.tipo_alimento_id)
            cesta_action = CestaAction(alimento.id, alimento.data_validade, tipo.nome, tipo.peso)
            details.append(cesta_action)
        return details

    @staticmethod
    def loadInfo(cesta):
        name = peso = data = ''
        try:
            name = Familia.loadFromId(cesta.id_familia).nome
            peso = CestaAction.calculatePeso(Alimento.loadAllEntitiesForCesta(cesta.id))
            entrega = Entrega.loadFromCestaId(cesta.id)
            data = CestaAction.getDateFormatted(entrega.data)
        except:
            pass
        return CestaAction(cesta.id, data, name, peso)

    @staticmethod
    def calculatePeso(alimentos):
        peso = 0
        for alimento in alimentos:
            tipo = TipoAlimento.loadFromId(alimento.tipo_alimento_id)
            peso = peso + tipo.peso
        return peso

    @staticmethod
    def getDateFormatted(input):
        input = date.fromisoformat(input)
        return f"{input.day}/{input.month}"
