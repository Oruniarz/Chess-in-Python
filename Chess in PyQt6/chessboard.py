from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QVBoxLayout, QPushButton, \
    QRadioButton, QWidget, QLineEdit
from PyQt6.QtGui import QPixmap, QPainter, QBrush, QColor, QPen, QPainterPath
from chess_piece import ChessPiece

class Chessboard(QGraphicsScene):
    def __init__(self, wielkosc):
        super().__init__()
        self.bierki = {}
        self.biale = {}
        self.czarne = {}
        self.wielkosc_pola = wielkosc
        self.turn = 2
        self.rysuj()

    def rysuj(self):
        self.setSceneRect(0, 0, self.wielkosc_pola * 8, self.wielkosc_pola * 8)
        for row in range(8):
            for col in range(8):
                x = col * self.wielkosc_pola
                y = row * self.wielkosc_pola
                if (row + col) % 2 == 0:
                    kolor = QColor("brown")
                else:
                    kolor = QColor("beige")
                self.addRect(x, y, self.wielkosc_pola, self.wielkosc_pola, QPen(QColor("black")), QBrush(kolor))
