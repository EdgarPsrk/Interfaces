# Grafica.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import QTimer
from ComunicacionSerial import ComunicacionSerial

class Grafica(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.comunicacion = ComunicacionSerial("/dev/ttyACM0", 9600)

        self.layout = QVBoxLayout(self)
        
        self.canvas_A0 = FigureCanvas(plt.Figure())
        self.layout.addWidget(self.canvas_A0)
        self.ax_A0 = self.canvas_A0.figure.add_subplot(111)
        self.line_A0, = self.ax_A0.plot([], [], label='A0')
        self.ax_A0.legend()

        self.canvas_A1 = FigureCanvas(plt.Figure())
        self.layout.addWidget(self.canvas_A1)
        self.ax_A1 = self.canvas_A1.figure.add_subplot(111)
        self.line_A1, = self.ax_A1.plot([], [], label='A1')
        self.ax_A1.legend()

        self.btn_conectar = QPushButton('Conectar', self)
        self.btn_conectar.clicked.connect(self.conectar_desconectar)
        self.layout.addWidget(self.btn_conectar)

        self.conectado = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_graficas)

    def conectar_desconectar(self):
        if not self.conectado:
            self.comunicacion.conectar()
            self.btn_conectar.setText('Desconectar')
            self.timer.start(100)
        else:
            self.comunicacion.desconectar()
            self.btn_conectar.setText('Conectar')
            self.timer.stop()

        self.conectado = not self.conectado

    def actualizar_graficas(self):
        datos_A0 = self.comunicacion.recibir_datos()
        datos_A1 = self.comunicacion.recibir_datos()

        if datos_A0 and datos_A1:
            valor_A0 = float(datos_A0)
            valor_A1 = float(datos_A1)

            self.actualizar_grafica(self.line_A0, self.ax_A0, valor_A0)
            self.actualizar_grafica(self.line_A1, self.ax_A1, valor_A1)

    def actualizar_grafica(self, line, ax, valor):
        x = list(line.get_xdata())
        y = list(line.get_ydata())

        x.append(len(x))
        y.append(valor)

        line.set_data(x, y)
        ax.relim()
        ax.autoscale_view()
        self.canvas_A0.draw()  # Agrega esta línea para redibujar la gráfica
        self.canvas_A1.draw()  # Agrega esta línea para redibujar la gráfica

