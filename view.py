from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QLineEdit, QPushButton, QTableWidgetItem, QMainWindow
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from controlador import Controller

import sys

class LoginView(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.controller = Controller()
        self.setup()
    
    def setup(self):
        self.botonLogin.clicked.connect(self.login)  
        self.campoPassword.setEchoMode(QLineEdit.Password)
    
    def login(self):
        usuario = self.campoUsuario.text()
        password = self.campoPassword.text()
        result = self.controller.existe(usuario, password) 
        if result == 1:
            self.menuView = MenuWindow(self)
            self.menuView.show()
            self.hide()
        elif result == 0:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("No existe un usuario con los \ndatos proporcionados")
            msgBox.setWindowTitle('Datos incorrectos')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec() 

# Creemos la clase para la segunda ventana, el menu principal

class MenuWindow(QMainWindow):
    def __init__(self, principal = None) -> None:
        super().__init__()
        uic.loadUi('mientras.ui', self)
        self.controlador = Controller()
        self.__ventanaPadre = principal
        self.setup()
    
    def setup(self):
        self.botonIngresar.clicked.connect(self.ingresarPaciente)
        self.botonBorrar.clicked.connect(self.borrarPaciente)
        self.botonSalirSis.clicked.connect(self.cerrar)
        self.clickver.clicked.connect(self.verPaciente)
        self.botonBuscar.clicked.connect(self.buscarPaciente)
        self.enviarActualizar1.clicked.connect(self.actualizarPaciente)

    def cerrar(self):
        self.close()
        self.__ventanaPadre.show()
        
    
    def ingresarPaciente(self):
        nombre = self.campoNombre.text()
        cc = str(self.campoCC.text())
        edad = self.campoEdad.text()
        patologia = self.campoPatologia.text()
        # print('vamo bien')
        resultado = self.controlador.existepaciente(cc)
        if resultado == 0:
            r = self.controlador.añadirPaciente(nombre, cc, edad, patologia)
            if r == 1:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText(f"Paciente Registrado \n con exito")
                msgBox.setWindowTitle('Añadido correctamente')
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec() 

        elif resultado == 1:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText(f"El paciente con {cc} \n ya esta registrado")
            msgBox.setWindowTitle('Datos incorrectos')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec() 
    
    def borrarPaciente(self,cc):
        cc = self.campoCCborrar.text()
        esta = self.controlador.existepaciente(cc)
        if esta == 1:
            r = self.controlador.borrarPaciente(cc)
            if r == 'removido':
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText(f"Paciente Eliminado \n con exito")
                msgBox.setWindowTitle('Eliminar Paciente')
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()
        elif esta == 0:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText(f"El paciente con {cc} \nno esta registrado")
                msgBox.setWindowTitle('Datos incorrectos')
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()


    def verPaciente(self):
        data = self.controlador.verPaciente() # retorna el json con los pacientes
        self.tablaPacientes.setRowCount(len(data))
        self.tablaPacientes.setColumnCount(4)
        self.tablaPacientes.setHorizontalHeaderLabels(['Nombre', 'CC', 'Edad', 'Patologia'])
        for row, paciente in enumerate(data):
            self.tablaPacientes.setItem(row, 0, QTableWidgetItem(paciente['Nombre']))
            self.tablaPacientes.setItem(row, 1, QTableWidgetItem(paciente['CC']))
            self.tablaPacientes.setItem(row, 2, QTableWidgetItem(str(paciente['Edad'])))
            self.tablaPacientes.setItem(row, 3, QTableWidgetItem(paciente['Patologia']))
    
    def buscarPaciente(self):
        query = self.nombreBuscar.text()  # Obtener el texto del QLineEdit
        if len(query) < 3:
            # Si la longitud del query es menor a 3, no hacer nada
            return
        
        data = self.controlador.verPaciente()  # Obtener todos los pacientes
        filtered_data = [p for p in data if p['Nombre'].lower().startswith(query[:3].lower())]
        
        # Configurar el QTableWidget con los resultados filtrados
        self.tablaPacientes.setRowCount(len(filtered_data))
        self.tablaPacientes.setColumnCount(4)
        self.tablaPacientes.setHorizontalHeaderLabels(['Nombre', 'CC', 'Edad', 'Patologia'])
        
        # Llenar el QTableWidget con los datos filtrados
        for row, paciente in enumerate(filtered_data):
            self.tablaPacientes.setItem(row, 0, QTableWidgetItem(paciente['Nombre']))
            self.tablaPacientes.setItem(row, 1, QTableWidgetItem(paciente['CC']))
            self.tablaPacientes.setItem(row, 2, QTableWidgetItem(str(paciente['Edad'])))
            self.tablaPacientes.setItem(row, 3, QTableWidgetItem(paciente['Patologia']))


    def actualizarPaciente(self):
        cc = str(self.ccActualizar.text())
        r = self.controlador.existepaciente(cc)
        if r == 1:
            # el paciente si esta
            self.controlador.borrarPaciente(cc)
            nombre = self.nombreActualizar.text()
            edad = self.edadActualizar.text()
            patologia = self.patologiaActualizar.text()
            r2 = self.controlador.añadirPaciente(nombre, cc, edad, patologia)
            if r2 == 1:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText(f"Paciente actualizado \n con exito")
                msgBox.setWindowTitle('Actualizar Paciente')
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()
            
        elif r == 0:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText(f"El paciente con {cc} \nno esta registrado\nVe a la pestaña de Nuevo Paciente")
            msgBox.setWindowTitle('Datos incorrectos')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()           



    

    
def main():
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        login_window = LoginView()
        login_window.show()
        sys.exit(app.exec_())

main()

            
