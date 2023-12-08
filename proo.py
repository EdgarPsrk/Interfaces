import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy

class MiVentana(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Creamos un botón
        boton_central = QPushButton('Centrado Horizontal', self)

        # Creamos un layout horizontal
        layout_horizontal = QHBoxLayout()

        # Agregamos un espacio flexible a la izquierda del botón
        spacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout_horizontal.addItem(spacer_left)

        # Agregamos el botón al layout
        layout_horizontal.addWidget(boton_central)

        # Agregamos un espacio flexible a la derecha del botón
        spacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout_horizontal.addItem(spacer_right)

        # Establecemos el layout de la ventana
        self.setLayout(layout_horizontal)

        self.setGeometry(300, 300, 400, 100)
        self.setWindowTitle('Centrado Horizontal')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MiVentana()
    sys.exit(app.exec_())
