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
        self.comunicacion.conectar()

        self.layout = QVBoxLayout(self)
        self.canvas = FigureCanvas(plt.Figure())
        self.layout.addWidget(self.canvas)

        self.ax = self.canvas.figure.add_subplot(111)
        self.line, = self.ax.plot([], [], label='Datos Arduino')
        self.ax.legend()

        self.animation = animation.FuncAnimation(self.canvas.figure, self.actualizar_grafica, blit=False, interval=100)

        self.btn_iniciar = QPushButton('Iniciar', self)
        self.btn_iniciar.clicked.connect(self.iniciar_animacion)
        self.layout.addWidget(self.btn_iniciar)

    def iniciar_animacion(self):
        self.animation.event_source.start()

    def actualizar_grafica(self,frame):
        datos = self.comunicacion.recibir_datos()
        if datos:
            valor = float(datos)
            x = list(self.line.get_xdata())
            y = list(self.line.get_ydata())

            x.append(len(x))
            y.append(valor)

            self.line.set_data(x, y)
            self.ax.relim()
            self.ax.autoscale_view()
            return self.line
        QTimer.singleShot(0, self.actualizar_grafica)