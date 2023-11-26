# Grafica.py
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSlider, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import QTimer, Qt
from ComunicacionSerial import ComunicacionSerial

des = '#7FFFD4'
con = '#CD5C5C'

class Grafica(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.comunicacion = ComunicacionSerial("/dev/ttyACM0", 9600)
        self.comunicacion.conectar()

        self.layout = QVBoxLayout(self)
        self.inicializar_ui()

        self.conectado = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_graficas)
        self.timer_envio_datos = QTimer(self)
        self.timer_envio_datos.timeout.connect(self.enviar_datos_desde_timer)
        self.setGeometry(300, 300, 800, 600)

    def inicializar_ui(self):
        self.layout_horizontal = QHBoxLayout()

        self.inicializar_grafica("A0")
        self.inicializar_grafica("A1")

        self.layout.addLayout(self.layout_horizontal)

        self.btn_conectar = QPushButton('Conectar', self)
        self.btn_conectar.clicked.connect(self.conectar_desconectar)
        self.layout.addWidget(self.btn_conectar, alignment=Qt.AlignHCenter)
        self.btn_conectar.setStyleSheet(f"background-color: {con}; border-radius: 10px; text-align: center;")
        self.btn_conectar.setFixedSize(100, 30)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 255)
        self.slider.valueChanged.connect(self.controlar_led)
        self.layout.addWidget(self.slider, alignment=Qt.AlignCenter)

        self.lbl_valor_slider = QLabel('Valor del Slider: 0', self)
        self.layout.addWidget(self.lbl_valor_slider, alignment=Qt.AlignCenter)

    def inicializar_grafica(self, nombre):
        canvas = FigureCanvas(plt.Figure())
        self.layout_horizontal.addWidget(canvas)
        ax = canvas.figure.add_subplot(111)
        line, = ax.plot([], [], label=nombre)
        ax.legend()

        setattr(self, f"canvas_{nombre}", canvas)
        setattr(self, f"ax_{nombre}", ax)
        setattr(self, f"line_{nombre}", line)

    def conectar_desconectar(self):
        if not self.conectado:
            self.comunicacion.conectar()
            self.btn_conectar.setText('Desconectar')
            self.btn_conectar.setStyleSheet(f"background-color: {des}; border-radius: 10px; text-align: center;")
            self.timer.start(100)
        else:
            self.comunicacion.desconectar()
            self.btn_conectar.setText('Conectar')
            self.btn_conectar.setStyleSheet(f"background-color: {con}; border-radius: 10px; text-align: center;")
            self.timer.stop()

        self.conectado = not self.conectado

    def actualizar_graficas(self):
        datos_A0 = self.comunicacion.recibir_datos()
        datos_A1 = self.comunicacion.recibir_datos()

        if datos_A0 and datos_A1:
            valor_A0 = float(datos_A0)
            valor_A1 = float(datos_A1)

            self.actualizar_grafica("A0", valor_A0)
            self.actualizar_grafica("A1", valor_A1)

    def actualizar_grafica(self, nombre, valor):
        line = getattr(self, f"line_{nombre}")
        ax = getattr(self, f"ax_{nombre}")

        x = list(line.get_xdata())
        y = list(line.get_ydata())

        max_puntos = 100

        x.append(len(x))
        y.append(valor)

        if len(x) > max_puntos:
            x = list(range(max_puntos))
            y = y[-max_puntos:]

        line.set_data(x, y)
        ax.relim()
        ax.autoscale_view()

        canvas = getattr(self, f"canvas_{nombre}")
        canvas.draw()

    def controlar_led(self, valor):
        if isinstance(valor, (int, float)):
            valor = int(valor)
            self.lbl_valor_slider.setText(f'Valor del Slider: {valor}')
            self.timer_envio_datos.start(100)

    def enviar_datos_desde_timer(self):
        valor = self.slider.value()
        self.comunicacion.enviar_datos(f'LED:{valor}')
        self.timer_envio_datos.stop()
