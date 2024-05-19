from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import QRectF


class ChessPiece(QGraphicsItem):
    def __init__(self, img_path, square_size, chess_type, chessboard):
        super().__init__()
        self.square_size = square_size
        self.current_pos = self.x(), self.y()
        self.future_pos = self.current_pos
        self.chess_type = chess_type
        self.chessboard = chessboard
        self.possible_moves = []
        self.possible_captures = []
        self.team = None
        self.has_moved = False

        self.img = QPixmap(img_path).scaled(self.square_size, self.square_size)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)

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
        # if (0 <= self.future_pos[0] <= 7 * self.square_size and
        #         0 <= self.future_pos[1] <= 7 * self.square_size and
        #         self.future_pos != self.current_pos):
        if self.future_pos in self.possible_moves:
            self.current_pos = self.future_pos
            self.setPos(self.future_pos[0], self.future_pos[1])
            self.has_moved = True
            self.chessboard.update_turn()
        elif self.future_pos in self.possible_captures:
            self.current_pos = self.future_pos
            self.setPos(self.future_pos[0], self.future_pos[1])
            self.has_moved = True
            self.chessboard.update_turn()
        else:
            self.future_pos = self.current_pos
            self.setPos(self.future_pos[0], self.future_pos[1])
        super().mouseReleaseEvent(event)

    def update_pos(self, online=False, future_pos=None):
        self.current_pos = self.x(), self.y()
        self.future_pos = self.current_pos

    def update_possible_moves(self):
        if self.team == "white":
            own_pieces = self.chessboard.white
            opponent_pieces = self.chessboard.black
            direction = -1
        elif self.team == "black":
            own_pieces = self.chessboard.black
            opponent_pieces = self.chessboard.white
            direction = 1
        match self.chessboard:
            case pawn if "pawn" in self.chess_type:
                (self.possible_moves,
                 self.possible_captures) = self.pawn_moves(own_pieces, opponent_pieces, direction)
            case rook if "rook" in self.chess_type:
                (self.possible_moves,
                 self.possible_captures) = self.rook_moves(own_pieces, opponent_pieces)
            case bishop if "bishop" in self.chess_type:
                (self.possible_moves,
                 self.possible_captures) = self.bishop_moves(own_pieces, opponent_pieces)
            case queen if "queen" in self.chess_type:
                (self.possible_moves,
                 self.possible_captures) = self.queen_moves(own_pieces, opponent_pieces)
            case knight if "knight" in self.chess_type:
                (self.possible_moves,
                 self.possible_captures) = self.knight_moves(own_pieces, opponent_pieces)
            case king if "king" in self.chess_type:
                pass

    def pawn_moves(self, own_pieces, opponent_pieces, direction):
        appr = True
        possible_moves = []
        possible_captures = []
        fut_pos = (self.current_pos[0], self.current_pos[1] + direction * self.square_size)
        if fut_pos[1] <= 7 * self.square_size:
            for piece in list(own_pieces.values()):
                if piece.current_pos == fut_pos:
                    appr = False
            for piece in list(opponent_pieces.values()):
                if piece.current_pos == fut_pos:
                    appr = False
            if appr:
                possible_moves.append(fut_pos)
                fut_pos = (self.current_pos[0], self.current_pos[1] + direction * 2 * self.square_size)
                appr = True
                if fut_pos[1] <= 7 * self.square_size and not self.has_moved:
                    for piece in list(own_pieces.values()):
                        if piece.current_pos == fut_pos:
                            appr = False
                    for piece in list(opponent_pieces.values()):
                        if piece.current_pos == fut_pos:
                            appr = False
                        if appr:
                            possible_moves.append(fut_pos)
        fut_pos = [(self.current_pos[0] - self.square_size,
                   self.current_pos[1] + direction * self.square_size),
                   (self.current_pos[0] + self.square_size,
                    self.current_pos[1] + direction * self.square_size)]
        for position in fut_pos:
            appr = False
            if 0 <= position[1] <= 7 * self.square_size and 0 <= position[0] <= 7 * self.square_size:
                for piece in list(opponent_pieces.values()):
                    if piece.current_pos == position:
                        appr = True
                if appr:
                    possible_captures.append(position)
                    pass
        return possible_moves, possible_captures

    def knight_moves(self, own_pieces, opponent_pieces):
        appr = True
        possible_moves = []
        possible_captures = []
        fut_pos = [
            (self.current_pos[0] + 2 * self.square_size, self.current_pos[1] + self.square_size),
            (self.current_pos[0] + 2 * self.square_size, self.current_pos[1] - self.square_size),
            (self.current_pos[0] - 2 * self.square_size, self.current_pos[1] + self.square_size),
            (self.current_pos[0] - 2 * self.square_size, self.current_pos[1] - self.square_size),
            (self.current_pos[0] + self.square_size, self.current_pos[1] + 2 * self.square_size),
            (self.current_pos[0] - self.square_size, self.current_pos[1] + 2 * self.square_size),
            (self.current_pos[0] + self.square_size, self.current_pos[1] - 2 * self.square_size),
            (self.current_pos[0] - self.square_size, self.current_pos[1] - 2 * self.square_size),
        ]
        for i, move in enumerate(fut_pos):
            appr = True
            if 0 <= move[0] <= 7 * self.square_size and 0 <= move[1] <= 7 * self.square_size:
                for piece in list(own_pieces.values()):
                    if piece.current_pos == move:
                        appr = False
                if appr:
                    for piece in list(opponent_pieces.values()):
                        if piece.current_pos == move:
                            appr = False
                    if appr:
                        possible_moves.append(move)
                    else:
                        possible_captures.append(move)
        return possible_moves, possible_captures

    def rook_moves(self, own_pieces, opponent_pieces):
        appr = True
        possible_moves = []
        possible_captures = []
        num_moves = int((7 * self.square_size - self.current_pos[0]) / self.square_size)
        for i in range(num_moves):  # all the moves to the right side of a board
            fut_pos = (self.current_pos[0] + (i + 1) * self.square_size, self.current_pos[1])
            for piece in list(own_pieces.values()):
                if piece.current_pos == fut_pos:
                    appr = False
            if appr:
                for piece in list(opponent_pieces.values()):
                    if piece.current_pos == fut_pos:
                        possible_captures.append(fut_pos)
                        appr = False
                if appr:
                    possible_moves.append(fut_pos)
        num_moves = int((self.current_pos[0]) / self.square_size)
        appr = True
        for i in range(num_moves):  # all the moves to the left side of a board
            fut_pos = (self.current_pos[0] - (i + 1) * self.square_size, self.current_pos[1])
            for piece in list(own_pieces.values()):
                if piece.current_pos == fut_pos:
                    appr = False
            if appr:
                for piece in list(opponent_pieces.values()):
                    if piece.current_pos == fut_pos:
                        possible_captures.append(fut_pos)
                        appr = False
                if appr:
                    possible_moves.append(fut_pos)
        num_moves = int((7 * self.square_size - self.current_pos[1]) / self.square_size)
        appr = True
        for i in range(num_moves):  # all the moves to the bottom side of a board
            fut_pos = (self.current_pos[0], self.current_pos[1] + (i + 1) * self.square_size)
            for piece in list(own_pieces.values()):
                if piece.current_pos == fut_pos:
                    appr = False
            if appr:
                for piece in list(opponent_pieces.values()):
                    if piece.current_pos == fut_pos:
                        possible_captures.append(fut_pos)
                        appr = False
                if appr:
                    possible_moves.append(fut_pos)
        num_moves = int((self.current_pos[1]) / self.square_size)
        appr = True
        for i in range(num_moves):  # all the moves to the top side of a board
            fut_pos = (self.current_pos[0], self.current_pos[1] - (i + 1) * self.square_size)
            for piece in list(own_pieces.values()):
                if piece.current_pos == fut_pos:
                    appr = False
            if appr:
                for piece in list(opponent_pieces.values()):
                    if piece.current_pos == fut_pos:
                        possible_captures.append(fut_pos)
                        appr = False
                if appr:
                    possible_moves.append(fut_pos)
        return possible_moves, possible_captures

    def bishop_moves(self, own_pieces, opponent_pieces):
        appr = True
        possible_moves = []
        possible_captures = []
        num_squares_to_right = int((7 * self.square_size - self.current_pos[0]) / self.square_size)
        num_squares_to_left = int((self.current_pos[0]) / self.square_size)
        for j in range(2):  # squares to the right side of a board
            appr = True
            for i in range(num_squares_to_right):
                if j == 0:  # top right squares
                    fut_pos = (self.current_pos[0] + (i + 1) * self.square_size,
                               self.current_pos[1] - (i + 1) * self.square_size)
                else:  # bottom right squares
                    fut_pos = (self.current_pos[0] + (i + 1) * self.square_size,
                               self.current_pos[1] + (i + 1) * self.square_size)
                for piece in list(own_pieces.values()):
                    if piece.current_pos == fut_pos:
                        appr = False
                if appr:
                    for piece in list(opponent_pieces.values()):
                        if piece.current_pos == fut_pos:
                            possible_captures.append(fut_pos)
                            appr = False
                    if appr:
                        possible_moves.append(fut_pos)
        for j in range(2):
            appr = True
            for i in range(num_squares_to_left):
                if j == 0:  # top left squares
                    fut_pos = (self.current_pos[0] - (i + 1) * self.square_size,
                               self.current_pos[1] - (i + 1) * self.square_size)
                else:  # bottom left squares
                    fut_pos = (self.current_pos[0] - (i + 1) * self.square_size,
                               self.current_pos[1] + (i + 1) * self.square_size)
                for piece in list(own_pieces.values()):
                    if piece.current_pos == fut_pos:
                        appr = False
                if appr:
                    for piece in list(opponent_pieces.values()):
                        if piece.current_pos == fut_pos:
                            possible_captures.append(fut_pos)
                            appr = False
                    if appr:
                        possible_moves.append(fut_pos)
        return possible_moves, possible_captures

    def queen_moves(self, own_pieces, opponent_pieces):
        queen_moves = []
        queen_captures = []
        possible_moves = []
        possible_captures = []
        possible_moves, possible_captures = self.bishop_moves(own_pieces, opponent_pieces)
        queen_moves, queen_captures = self.rook_moves(own_pieces, opponent_pieces)
        for move in queen_moves:
            possible_moves.append(move)
        for capture in queen_captures:
            possible_captures.append(capture)
        return possible_moves, possible_captures
