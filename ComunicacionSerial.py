# ComunicacionSerial.py
import serial

class ComunicacionSerial:
    def __init__(self, puerto, baudios):
        self.puerto = puerto
        self.baudios = baudios
        self.conexion = None

    def conectar(self):
        try:
            self.conexion = serial.Serial(self.puerto, self.baudios, timeout=1)
            print(f"Conectado al puerto {self.puerto}")
        except serial.SerialException as e:
            print(f"Error de conexión: {e}")

    def desconectar(self):
        if self.conexion and self.conexion.isOpen():
            self.conexion.close()
            print("Desconectado")

    def enviar_datos(self, datos):
        if self.conexion and self.conexion.isOpen():
            self.conexion.write(datos.encode())
            print(f"Datos enviados: {datos}")

    def recibir_datos(self):
        if self.conexion and self.conexion.isOpen():
            return self.conexion.readline().decode().strip()

    def cerrar_puerto(self):
        if self.conexion and self.conexion.isOpen():
            self.conexion.close()
