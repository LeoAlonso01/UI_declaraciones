import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ejemplo de PyQt')

        self.setGeometry(100, 100,  400, 300)
        self.label = QLabel('Presiona el botón', self)
        self.button = QPushButton('Presionar', self)
        self.button.clicked.connect(self.on_button_click)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def on_button_click(self):
        self.label.setText('¡Hola, PyQt!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
