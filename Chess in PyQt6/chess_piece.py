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
        self.move_piece()
        super().mouseReleaseEvent(event)

    def move_piece(self):
        if self.future_pos in self.possible_moves:
            if self.chess_type == "king":
                if self.future_pos[0] == self.current_pos[0] + 2 * self.square_size:  # castling to the right
                    rook = self.chessboard.pieces[self.team]["rook1"]
                    rook.setPos(self.future_pos[0] - self.square_size, self.future_pos[1])
                    rook.current_pos = (self.future_pos[0] - self.square_size, self.future_pos[1])
                    rook.has_moved = True
                    self.current_pos = self.future_pos
                    self.setPos(self.future_pos[0], self.future_pos[1])
                    self.has_moved = True
                elif self.future_pos[0] == self.current_pos[0] - 2 * self.square_size:  # castling to the left
                    rook = self.chessboard.pieces[self.team]["rook0"]
                    rook.setPos(self.future_pos[0] + self.square_size, self.future_pos[1])
                    rook.current_pos = (self.future_pos[0] + self.square_size, self.future_pos[1])
                    rook.has_moved = True
                    self.current_pos = self.future_pos
                    self.setPos(self.future_pos[0], self.future_pos[1])
                    self.has_moved = True
                else:  # "normal" move
                    self.current_pos = self.future_pos
                    self.setPos(self.future_pos[0], self.future_pos[1])
                    self.has_moved = True
            else:  # pieces other than king
                self.current_pos = self.future_pos
                self.setPos(self.future_pos[0], self.future_pos[1])
                self.has_moved = True
            self.chessboard.update_turn()
        elif self.future_pos in self.possible_captures:  # capturing
            self.current_pos = self.future_pos
            self.setPos(self.future_pos[0], self.future_pos[1])
            self.has_moved = True
            self.chessboard.update_turn()
        else:  # move not allowed
            self.future_pos = self.current_pos
            self.setPos(self.future_pos[0], self.future_pos[1])

    def update_pos(self, online=False, future_pos=None):  # function for updating position during the initialization of chessboard
        self.current_pos = self.x(), self.y()
        self.future_pos = self.current_pos

    def update_possible_moves(self):  # function for updating possible moves of a piece
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
                (self.possible_moves,
                 self.possible_captures) = self.king_moves(own_pieces, opponent_pieces)

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
                if (0 <= fut_pos[0] <= 7 * self.square_size
                        and 0 <= fut_pos[1] <= 7 * self.square_size):
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
                if 0 <= fut_pos[0] <= 7 * self.square_size and 0 <= fut_pos[1] <= 7 * self.square_size:
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

    def king_moves(self, own_pieces, opponent_pieces):
        possible_moves = []
        possible_captures = []
        appr = True
        fut_pos = [
            (self.current_pos[0], self.current_pos[1] + self.square_size),
            (self.current_pos[0] - self.square_size, self.current_pos[1] + self.square_size),
            (self.current_pos[0] - self.square_size, self.current_pos[1] - self.square_size),
            (self.current_pos[0], self.current_pos[1] - self.square_size),
            (self.current_pos[0] + self.square_size, self.current_pos[1] - self.square_size),
            (self.current_pos[0] + self.square_size, self.current_pos[1] + self.square_size),
        ]
        fut_pos_with_castling = [
            (self.current_pos[0] - self.square_size, self.current_pos[1]),
            (self.current_pos[0] + self.square_size, self.current_pos[1]),
        ]
        for move in fut_pos:  # move in every direction except to the right and to the left
            if (0 <= move[0] <= 7 * self.square_size
                    and 0 <= move[1] <= 7 * self.square_size):
                appr = True
                for piece in list(own_pieces.values()):
                    if piece.current_pos == move:
                        appr = False
                if appr:
                    for piece in list(opponent_pieces.values()):
                        if piece.current_pos == move:
                            possible_captures.append(move)
                            appr = False
                    if appr:
                        possible_moves.append(move)
        for move in fut_pos_with_castling:  # move to the right, to the left and castling
            if (0 <= move[0] <= 7 * self.square_size
                    and 0 <= move[1] <= 7 * self.square_size):
                appr = True
                for piece in list(own_pieces.values()):
                    if piece.current_pos == move:
                        appr = False
                if appr:
                    for piece in list(opponent_pieces.values()):
                        if piece.current_pos == move:
                            possible_captures.append(move)
                            appr = False
                    if appr:
                        possible_moves.append(move)
                        if not self.has_moved:  # castling
                            if (move[0] - self.current_pos[0] > 0
                                    and not own_pieces["rook1"].has_moved):  # castling to the right
                                move2 = (move[0] + self.square_size, move[1])
                                for piece in list(own_pieces.values()):
                                    if piece.current_pos == move2:
                                        appr = False
                                for piece in list(opponent_pieces.values()):
                                    if piece.current_pos == move2:
                                        appr = False
                                if appr:
                                    possible_moves.append((move[0] + 1 * self.square_size, move[1]))
                            elif (move[0] - self.current_pos[0] < 0
                                    and not own_pieces["rook0"].has_moved):  # castling to the left
                                fut_pos = [
                                    (move[0] - self.square_size, move[1]),
                                    (move[0] - 2 * self.square_size, move[1]),
                                ]
                                for move2 in fut_pos:
                                    for piece in list(own_pieces.values()):
                                        if piece.current_pos == move2:
                                            appr = False
                                    for piece in list(opponent_pieces.values()):
                                        if piece.current_pos == move2:
                                            appr = False
                                if appr:
                                    possible_moves.append((move[0] - 1 * self.square_size, move[1]))
        return possible_moves, possible_captures

