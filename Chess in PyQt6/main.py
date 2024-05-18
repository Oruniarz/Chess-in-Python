import sys

from PyQt6.QtWidgets import (QApplication, QGraphicsView, QVBoxLayout, QPushButton,
                             QRadioButton, QWidget, QLineEdit, QLabel)
from chessboard import Chessboard

DATA_SIZE = 2000
HOST = "localhost"
PORT = 80
SERVER_ADDRESS = (HOST, PORT)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.view = QGraphicsView()
        self.scene = None
        self.square_size = 75
        self.initUI()
        self.setWindowTitle("Game Info")

    def initUI(self):
        self.layout = QVBoxLayout()

        self.radio_one_player = QRadioButton("Jeden gracz", )
        self.radio_two_players = QRadioButton("Dwóch graczy")
        self.radio_vs_computer = QRadioButton("Przeciwko AI")

        self.square_size_label = QLabel("Square size:")
        self.square_size_line = QLineEdit(str(self.square_size))

        self.ip_label = QLabel("IP:")
        self.ip_line = QLineEdit(HOST)

        self.port_label = QLabel("Port:")
        self.port_line = QLineEdit(str(PORT))

        self.radio_one_player.setChecked(True)

        self.button = QPushButton("Ok")
        self.button.clicked.connect(self.load_chessboard)

        self.layout.addWidget(self.radio_one_player)
        self.layout.addWidget(self.radio_two_players)
        self.layout.addWidget(self.radio_vs_computer)
        self.layout.addWidget(self.square_size_label)
        self.layout.addWidget(self.square_size_line)
        self.layout.addWidget(self.ip_label)
        self.layout.addWidget(self.ip_line)
        self.layout.addWidget(self.port_label)
        self.layout.addWidget(self.port_line)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def load_chessboard(self):
        option = "1 player"
        if self.radio_one_player.isChecked():
            option = "1 player"
        elif self.radio_two_players.isChecked():
            option = "2 player"
        elif self.radio_vs_computer.isChecked():
            option = "vs computer"

        self.square_size = int(self.square_size_line.text())
        ip = self.ip_line.text()
        port = int(self.port_line.text())

        if not self.scene:
            self.scene = Chessboard(square_size=self.square_size)
            self.view.setScene(self.scene)
            self.view.setWindowTitle("Chessboard")
            self.view.show()
            self.hide()


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
