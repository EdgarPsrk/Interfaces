# Grafica.py
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSlider, QLabel,QDial,QLCDNumber
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
#LAYOUT
        self.layout_graficas = QHBoxLayout()
        self.layout_slider_boton = QHBoxLayout()
        self.layout_slider = QVBoxLayout()
        self.layout_boton = QVBoxLayout()
        self.layout_lcd = QVBoxLayout()
#GrAFICAS
        self.inicializar_grafica("A0")
        self.inicializar_grafica("A1")
#BOTONES
        self.btn_conectar = QPushButton('Conectar', self)
        self.btn_conectar.clicked.connect(self.conectar_desconectar)
        self.btn_conectar.setStyleSheet(f"background-color: {slateGray}; border-radius: 10px; text-align: center;")
        self.btn_conectar.setFixedSize(100, 30)

        self.btn_pausar = QPushButton('Pausar', self)
        self.btn_pausar.clicked.connect(self.pausar_graficas)
        self.btn_pausar.setStyleSheet(f"background-color: {slateGray}; border-radius: 10px; text-align: center;")
        self.btn_pausar.setFixedSize(100, 30)

#DIAL
        self.dial_ledA = QDial()
        self.dial_ledA.setRange(0, 255)
        self.dial_ledA.valueChanged.connect(self.control_ledA)
        #self.dial_ledA.setFixedSize(100, 30)

        
        self.valor_dialA = QLCDNumber(self)
        self.valor_dialA.setFixedSize(100, 30)
        #self.valor_dialA.setStyleSheet(f"background-color: {slateGray}; border-radius: 10px; text-align: center; color = {violetRed};")



        self.dial_ledB = QDial()
        self.dial_ledB.setRange(0, 255)
        self.dial_ledB.valueChanged.connect(self.control_ledB)
        #self.dial_ledB.setFixedSize(100, 30)

        self.valor_dialB = QLCDNumber(self)
        self.valor_dialB.setFixedSize(100, 30)
        #self.valor_dialB.setStyleSheet(f"background-color: {slateGray}; border-radius: 10px; text-align: center; color = {violetRed};")


        
#AGREGANDO
        self.layout_principal.addLayout(self.layout_graficas)

        self.layout_boton.addWidget(self.btn_conectar, alignment=Qt.AlignBottom | Qt.AlignRight )
        self.layout_boton.addWidget(self.btn_pausar,   alignment=Qt.AlignBottom | Qt.AlignRight )
        self.layout_slider.addWidget(self.dial_ledA,   alignment=Qt.AlignBottom | Qt.AlignRight )
        self.layout_lcd.addWidget(self.valor_dialA,    alignment=Qt.AlignBottom | Qt.AlignLeft )
        self.layout_slider.addWidget(self.dial_ledB,   alignment=Qt.AlignBottom | Qt.AlignRight )
        self.layout_lcd.addWidget(self.valor_dialB,    alignment=Qt.AlignBottom | Qt.AlignLeft )

        # self.layout_boton.addWidget(self.btn_conectar, alignment=Qt.AlignCenter )
        # self.layout_boton.addWidget(self.btn_pausar,   alignment=Qt.AlignCenter )
        # self.layout_slider.addWidget(self.dial_ledA,   alignment=Qt.AlignCenter )
        # self.layout_lcd.addWidget(self.valor_dialA,    alignment=Qt.AlignCenter )
        # self.layout_slider.addWidget(self.dial_ledB,   alignment=Qt.AlignCenter )
        # self.layout_lcd.addWidget(self.valor_dialB,    alignment=Qt.AlignCenter )




        # self.layout_lcd.setContentsMargins(0,0,0,0)
        # self.layout_boton.setContentsMargins(0,0,0,0)
        # self.layout_slider.setContentsMargins(0,0,0,0)

        # self.btn_conectar.setLayout(self.layout_boton)
        # self.btn_pausar.setLayout(self.layout_boton)
        # self.dial_ledA.setLayout(self.layout_slider)
        # self.dial_ledB.setLayout(self.layout_slider)
        # self.valor_dialA.setLayout(self.layout_lcd)
        # self.valor_dialB.setLayout(self.layout_lcd)

        # self.layout_slider_boton.addLayout(self.layout_boton)
        # self.layout_slider_boton.addLayout(self.layout_slider)
        # self.layout_slider_boton.addLayout(self.layout_lcd)
        # self.layout_principal.addLayout(self.layout_slider_boton)

        # self.layout_boton.addStretch()
        # self.layout_slider.addStretch()
        # self.layout_lcd.addStretch()




        self.layout_slider_boton.addLayout(self.layout_boton)
        self.layout_slider_boton.addLayout(self.layout_slider)
        self.layout_slider_boton.addLayout(self.layout_lcd)
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
            self.valor_dialA.display(valor)
            self.timer_envio_datosA.start(100)

    def enviar_datos_timerA(self):
        valor = self.dial_ledA.value()
        self.comunicacion.enviar_datos(f'LED1:{valor}\n')
        self.timer_envio_datosA.stop()


    def control_ledB(self, valor):
        if isinstance(valor, (int, float)):
            valor = int(valor)
            self.valor_dialB.display(valor)
            self.timer_envio_datosB.start(100)

#enviar datos desde el timer para el led
    def enviar_datos_timerB(self):
        valor = self.dial_ledB.value()
        self.comunicacion.enviar_datos(f'LED2:{valor}\n')
        self.timer_envio_datosB.stop()