import json

class Model:
    def __init__(self, users_file = 'users.json', pacientes = 'pacientes.json' ):
        self.users = users_file
        self.pacientes = pacientes
        self.load()
        self.loadPacientes()
    
    def load(self):
        try:
            with open(self.users, 'r') as file:
                self.users = json.load(file)
        except FileNotFoundError:
            self.users = []
            print("Parece que no hay un archivo que ver...")
    
    def validate_user(self, user, password):
        try:
            for i in self.users['usuarios']:
                if i['user'] == user and i['password'] == password:
                    return 1
            return 0
        except TypeError:
            return 2
        
    def loadPacientes(self):
        try:
            with open('pacientes.json', 'r') as file:
                self.pacientes = json.load(file)
        except FileNotFoundError:
            self.pacientes = []
            print("Parece que no hay un archivo que ver...")

    def validarExistente(self, cc):
        r = []
        try:
            for i in self.pacientes:  #  1 si esta. 0 si no esta
                if cc == i['CC']:
                    r.append(1)
        except TypeError:
            return 2
        if len(r)>0:
            return 1
        elif len(r) == 0:
            return 0
        
    def añadirPaciente(self, nombre, cc, edad, patologia):
        nuevo_paciente = {
            "Nombre": nombre,
            "CC": cc,
            "Edad": edad,
            "Patologia": patologia
            }
        self.pacientes.append(nuevo_paciente)
        with open('pacientes.json','w') as file:
            json.dump(self.pacientes, file, indent=4, ensure_ascii=False)
        return 1

    def borrarPaciente(self,cc):
        for i in self.pacientes:
            if cc == i['CC']:
                self.pacientes = [paciente for paciente in self.pacientes if paciente['CC'] != cc]
                with open('pacientes.json', 'w') as file:
                    json.dump(self.pacientes, file, indent=4, ensure_ascii=False)
                    return 'removido'

    def verPaciente(self):
        return self.pacientes
