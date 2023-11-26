from PyQt5.QtCore import QTimer

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSlider, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from ComunicacionSerial import ComunicacionSerial


crimson = '#DC143C'
seaGreen = '#2E8B57'

steelBlue = '#4682B4'
slateGray = '#708090'

violetRed = '#DB7093'


class MiVentana(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()
        self.comunicacion = ComunicacionSerial("/dev/ttyACM0", 9600)
        self.comunicacion.conectar()
        
    def initUI(self):
        # Crear componentes
        canvas_A0 = self.crear_grafica()
        canvas_A1 = self.crear_grafica()
        
        slider_uno = self.crear_slider()
        slider_dos = self.crear_slider()

        btn_uno = self.crear_boton('Conectar', slateGray)
        btn_dos = self.crear_boton('Pausar', slateGray)
        btn_tres = self.crear_boton('Reiniciar', slateGray)

        # Configurar el diseño
        layout_principal = QVBoxLayout()
        layout_graficas = QHBoxLayout()
        layout_sliders_botones = QHBoxLayout()
        layout_sliders = QVBoxLayout()
        layout_botones = QVBoxLayout()

        layout_graficas.addWidget(canvas_A0)
        layout_graficas.addWidget(canvas_A1)

        layout_sliders.addWidget(slider_uno)
        layout_sliders.addWidget(slider_dos)

        layout_botones.addWidget(btn_uno)
        layout_botones.addWidget(btn_dos)
        layout_botones.addWidget(btn_tres)

        # Limitar el tamaño de los botones
        for boton in [btn_uno, btn_dos, btn_tres]:
            boton.setFixedSize(100, 30)

        # Agregar los componentes al diseño principal
        layout_principal.addLayout(layout_graficas)
        layout_sliders_botones.addLayout(layout_sliders)
        layout_sliders_botones.addLayout(layout_botones)
        layout_principal.addLayout(layout_sliders_botones)

        # Aplicar el diseño al widget principal
        self.setLayout(layout_principal)

        #self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Instrumentacion')

        self.conectado = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_graficas)

    def crear_grafica(self):
        self.canvas = FigureCanvas(plt.Figure())
        self.ax = self.canvas.figure.add_subplot(111)
        self.line = self.ax.plot( [], [], label = 'Grafica')
        self.ax.legend()

        return self.canvas

    def crear_slider(self):
        slider = QSlider()
        slider.setOrientation(1)  # 2 significa orientación vertical
        slider.setFixedSize(750, 50)  # Tamaño fijo del slider
        return slider

    def crear_boton(self, texto, color):
        btn = QPushButton(texto, self)
        btn.setStyleSheet(f"background-color: {color}; border-radius: 10px;")


        if (texto == 'Conectar'):
            self.btn.clicked.connect(self.conectar_desconectar)
            
        elif(texto == 'Pausar' ):
            self.btn.clicked.connect(self.pausar)
            
        else:
            self.btn.clicked.connect(self.reset)
            
        return btn


    def conectar_desconectar(self):
        if not self.conectado:
            self.comunicacion.conectar()
            self.btn.setText('Desconectar')
            self.btn.setStyleSheet(f'background-color: {seaGreen}')
            self.timer.start(100)
        else:
            self.comunicacion.desconectar()
            self.btn.setText('Conectar')
            self.btn.setStyleSheet(f'background-color: {crimson}')
            self.timer.stop()

        self.conectado = not self.conectado


    def actualizar_graficas(self):
        datos = self.comunicacion.recibir_datos()
        #datos_A1 = self.comunicacion.recibir_datos()

        if datos:
            valor = float(datos)
            #valor_A1 = float(datos_A1)

            self.actualizar_grafica(self.line, self.ax, valor)
            #self.actualizar_grafica(self.line_A1, self.ax_A1, valor_A1)

    def actualizar_grafica(self, line, ax, valor):
        x = list(line.get_xdata())
        y = list(line.get_ydata())

        max_puntos = 200  # Número máximo de puntos en la gráfica

        x.append(len(x))
        y.append(valor)

        if len(x) > max_puntos:
            x = x[-max_puntos:]
            y = y[-max_puntos:]

        line.set_data(x, y)
        ax.relim()
        ax.autoscale_view()
        self.canvas.draw()
        #self.canvas_A1.draw()


def pausar(self,texto):
    if(texto==pausar):
        self.btn.setText('Reanudar')
        self.btn.setStyleSheet(f'background-color: {slateGray}')


    else:
        self.btn.setText('Pausar')
        self.btn.setStyleSheet(f'background-color: {steelBlue}')


def reanudar(self,texto):
        self.btn.setStyleSheet(f'background-color: {violetRed}')
    