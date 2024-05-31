from PyQt5 import QtWidgets
from model import * 

class Controller:
    def __init__(self):
        self.model = Model()
        
        # Conectar señales de la vista a métodos del controlador
        
    def show_view(self):
        self.view.show()
    
    def existe(self, username: str, password: str):
        result = self.model.validate_user(username, password) # retorna 1 si esta, 0 si no
        return result
    
    def existepaciente(self, cc):
        return self.model.validarExistente(cc)    # resultado va a ser 1 si no esta, 0 si si esta
    
    def añadirPaciente(self, nombre, cc, edad, patologia):
        resultado = self.model.añadirPaciente(nombre, cc, edad, patologia)
        return resultado
    
    def borrarPaciente(self,cc):
        return self.model.borrarPaciente(cc)
    
    def verPaciente(self):
        return self.model.verPaciente()
