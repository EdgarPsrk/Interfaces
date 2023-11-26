# main.py
import sys
from PyQt5.QtWidgets import QApplication
from sintax import MiVentana

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec_())
