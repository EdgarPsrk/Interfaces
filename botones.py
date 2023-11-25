import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout

class MiVentana(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Crea seis botones
        btn1 = self.crear_boton('Botón 1', 'blue')
        btn2 = self.crear_boton('Botón 2', 'green')
        btn3 = self.crear_boton('Botón 3', 'red')
        btn4 = self.crear_boton('Botón 4', 'yellow')
        btn5 = self.crear_boton('Botón 5', 'purple')
        btn6 = self.crear_boton('Botón 6', 'orange')

        # Configura el tamaño máximo para cada botón
        btn1.setMaximumSize(100, 30)
        btn2.setMaximumSize(100, 30)
        btn3.setMaximumSize(100, 30)
        btn4.setMaximumSize(100, 30)
        btn5.setMaximumSize(100, 30)
        btn6.setMaximumSize(100, 30)

        # Configura el diseño horizontal
        layout_horizontal = QHBoxLayout()

        # Configura el diseño vertical para los primeros tres botones
        layout_vertical1 = QVBoxLayout()
        layout_vertical1.addWidget(btn1)
        layout_vertical1.addWidget(btn2)
        layout_vertical1.addWidget(btn3)

        # Configura el diseño vertical para los últimos tres botones
        layout_vertical2 = QVBoxLayout()
        layout_vertical2.addWidget(btn4)
        layout_vertical2.addWidget(btn5)
        layout_vertical2.addWidget(btn6)

        # Agrega los diseños verticales al diseño horizontal
        layout_horizontal.addLayout(layout_vertical1)
        layout_horizontal.addLayout(layout_vertical2)

        # Aplica el diseño al widget principal
        self.setLayout(layout_horizontal)

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Botones en PyQt5')

    def crear_boton(self, texto, color):
        btn = QPushButton(texto, self)
        btn.setStyleSheet(f"background-color: {color}")
        return btn

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec_())
