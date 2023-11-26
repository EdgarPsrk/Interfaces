# main.py
import sys
from PyQt5.QtWidgets import QApplication
from Grafica import Grafica

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Grafica()
    ventana.show()
    sys.exit(app.exec_())
