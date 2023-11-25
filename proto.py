import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSlider, QPushButton
from PyQt5.QtGui import QPalette, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class MiVentana(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Crear componentes
        self.canvas1 = self.crear_grafica()
        self.canvas2 = self.crear_grafica()
        
        slider1 = self.crear_slider_vertical()
        slider2 = self.crear_slider_vertical()

        boton1 = self.crear_boton('Botón 1', 'blue')
        boton2 = self.crear_boton('Botón 2', 'green')
        boton3 = self.crear_boton('Botón 3', 'red')
        boton4 = self.crear_boton('Botón 4', 'yellow')

        # Configurar el diseño
        layout_principal = QVBoxLayout()

        # Espacio para las gráficas
        layout_graficas = QHBoxLayout()
        layout_graficas.addWidget(self.canvas1)
        layout_graficas.addWidget(self.canvas2)

        # Dividir el espacio para los sliders y botones
        layout_sliders_botones = QHBoxLayout()

        # Espacio para los sliders (ahora en una disposición vertical)
        layout_sliders = QVBoxLayout()
        layout_sliders.addWidget(slider1)
        layout_sliders.addWidget(slider2)

        # Espacio para los botones
        layout_botones = QVBoxLayout()
        layout_botones.addWidget(boton1)
        layout_botones.addWidget(boton2)
        layout_botones.addWidget(boton3)
        layout_botones.addWidget(boton4)

        # Limitar el tamaño de los botones
        for boton in [boton1, boton2, boton3, boton4]:
            boton.setFixedSize(100, 30)

        # Agregar los componentes al diseño principal
        layout_principal.addLayout(layout_graficas)
        layout_sliders_botones.addLayout(layout_sliders)
        layout_sliders_botones.addLayout(layout_botones)
        layout_principal.addLayout(layout_sliders_botones)

        # Aplicar el diseño al widget principal
        self.setLayout(layout_principal)

        #self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Interfaz con Gráficas, Sliders y Botones')

    def crear_grafica(self):
        fig, ax = plt.subplots()
        canvas = FigureCanvas(fig)
        return canvas

    def crear_slider_vertical(self):
        slider = QSlider()
        slider.setOrientation(1)  # 2 significa orientación vertical
        slider.setFixedSize(750, 50)  # Tamaño fijo del slider
        return slider

    def crear_boton(self, texto, color):
        btn = QPushButton(texto, self)
        btn.setStyleSheet(f"background-color: {color}; border-radius: 10px;")
        return btn

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec_())
