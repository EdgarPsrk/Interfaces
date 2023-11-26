# Grafica.py
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSlider, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import QTimer, Qt
from ComunicacionSerial import ComunicacionSerial

crimson = '#DC143C'
seaGreen = '#2E8B57'

steelBlue = '#4682B4'
slateGray = '#708090'
violetRed = '#DB7093'

des = '#7FFFD4'
con = '#CD5C5C'

class Grafica(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.comunicacion = ComunicacionSerial("/dev/ttyACM0", 9600)
        self.comunicacion.conectar()

        self.layout_principal = QVBoxLayout(self)
        self.inicializar_ui()

        self.conectado = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_graficas)
        self.timer_envio_datosA = QTimer(self)
        self.timer_envio_datosA.timeout.connect(self.enviar_datos_timerA)
        self.timer_envio_datosB = QTimer(self)
        self.timer_envio_datosB.timeout.connect(self.enviar_datos_timerB)
        self.setGeometry(300, 300, 800, 600)

    def inicializar_ui(self):
        self.layout_graficas = QHBoxLayout()
        self.layout_slider_boton = QHBoxLayout()
        self.layout_slider = QVBoxLayout()
        self.layout_boton = QVBoxLayout()


        self.inicializar_grafica("A0")
        self.inicializar_grafica("A1")

        self.layout_principal.addLayout(self.layout_graficas)

        self.btn_conectar = QPushButton('Conectar', self)
        self.btn_conectar.clicked.connect(self.conectar_desconectar)
        self.layout_boton.addWidget(self.btn_conectar, alignment=Qt.AlignCenter)
        self.btn_conectar.setStyleSheet(f"background-color: {slateGray}; border-radius: 10px; text-align: center;")
        self.btn_conectar.setFixedSize(100, 30)

        self.btn_pausar = QPushButton('Pausar', self)
        self.btn_pausar.clicked.connect(self.pausar_graficas)
        self.layout_boton.addWidget(self.btn_pausar, alignment=Qt.AlignCenter)
        self.btn_pausar.setStyleSheet(f"background-color: {slateGray}; border-radius: 10px; text-align: center;")
        self.btn_pausar.setFixedSize(100, 30)

        self.slider_ledA = QSlider(Qt.Horizontal)
        self.slider_ledA.setRange(0, 255)
        self.slider_ledA.valueChanged.connect(self.control_ledA)
        self.layout_slider.addWidget(self.slider_ledA, alignment=Qt.AlignCenter)

        self.valor_sliderA = QLabel('Valor del Slider: 0', self)
        self.layout_slider.addWidget(self.valor_sliderA, alignment=Qt.AlignCenter)

        self.slider_ledB = QSlider(Qt.Horizontal)
        self.slider_ledB.setRange(0, 255)
        self.slider_ledB.valueChanged.connect(self.control_ledB)
        self.layout_slider.addWidget(self.slider_ledB, alignment=Qt.AlignCenter)

        self.valor_sliderB = QLabel('Valor del Otro LED: 0', self)
        self.layout_slider.addWidget(self.valor_sliderB, alignment=Qt.AlignCenter)

        self.layout_slider_boton.addLayout(self.layout_boton)
        self.layout_slider_boton.addLayout(self.layout_slider)
        self.layout_principal.addLayout(self.layout_slider_boton)


    def inicializar_grafica(self, nombre):
        canvas = FigureCanvas(plt.Figure())
        self.layout_graficas.addWidget(canvas)
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
        if not self.timer.isActive():
            return

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
        max_puntos = 100

        x = list(line.get_xdata())
        y = list(line.get_ydata())

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



    def pausar_graficas(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn_pausar.setText('Reanudar')
            self.btn_pausar.setStyleSheet(f"background-color: {steelBlue}; color:white; border-radius: 10px; text-align: center;")
        else:
            self.timer.start(100)
            self.btn_pausar.setText('Pausar')
            self.btn_pausar.setStyleSheet(f"background-color: {seaGreen}; color:white; border-radius: 10px; text-align: center;")



    def control_ledA(self, valor):
        if isinstance(valor, (int, float)):
            valor = int(valor)
            self.valor_sliderA.setText(f'Valor del Slider: {valor}')
            self.timer_envio_datosA.start(100)

    def enviar_datos_timerA(self):
        valor = self.slider_ledA.value()
        self.comunicacion.enviar_datos(f'LED1:{valor}\n')
        self.timer_envio_datosA.stop()


    def control_ledB(self, valor):
        if isinstance(valor, (int, float)):
            valor = int(valor)
            self.valor_sliderB.setText(f'Valor del Otro LED: {valor}')
            self.timer_envio_datosB.start(100)

#enviar datos desde el timer para el led
    def enviar_datos_timerB(self):
        valor = self.slider_ledB.value()
        self.comunicacion.enviar_datos(f'LED2:{valor}\n')
        self.timer_envio_datosB.stop()