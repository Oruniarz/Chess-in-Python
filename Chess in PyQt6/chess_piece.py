from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import QRectF


class ChessPiece(QGraphicsItem):
    def __init__(self, img_path, square_size, chess_type):
        super().__init__()
        self.square_size = square_size
        self.current_pos = self.x(), self.y()
        self.future_pos = self.current_pos
        self.chess_type = chess_type

        self.img = QPixmap(img_path).scaled(self.square_size, self.square_size)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

    def boundingRect(self):
        bounds = self.square_size
        return QRectF(0, 0, bounds, bounds)

    def paint(self, painter: QPainter, option, widget=None):
        painter.drawPixmap(0, 0, self.img)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if bool(self.flags() & QGraphicsItem.GraphicsItemFlag.ItemIsMovable):
            self.setScale(1.2)

    def mouseReleaseEvent(self, event):
        self.setScale(1)
        x_round = round(self.x() / self.square_size) * self.square_size
        y_round = round(self.y() / self.square_size) * self.square_size
        self.future_pos = x_round, y_round
        if (0 <= self.future_pos[0] <= 7 * self.square_size and
                0 <= self.future_pos[1] <= 7 * self.square_size):
            self.current_pos = self.future_pos
            self.setPos(self.future_pos[0], self.future_pos[1])
            super().mouseReleaseEvent(event)
        else:
            self.future_pos = self.current_pos
            self.setPos(self.future_pos[0], self.future_pos[1])
            super().mouseReleaseEvent(event)

    def update_pos(self, online=False, future_pos=None):
        self.current_pos = self.x(), self.y()
        self.future_pos = self.current_pos
