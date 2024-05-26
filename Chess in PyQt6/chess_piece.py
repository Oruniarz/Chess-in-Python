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
        self.check = False
        self.own_pieces = None
        self.opponent_pieces = None

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
        """Function that moves given piece and checks if it is allowed"""

        if self.future_pos in self.possible_moves:
            if self.chess_type == "king":
                if self.future_pos[0] == self.current_pos[0] + 2 * self.square_size:  # castling to the right
                    if "rook1" in self.own_pieces.keys():
                        rook = self.chessboard.pieces[self.team]["rook1"]
                        if not self.check_for_checks(castling="right"):
                            rook.setPos(rook.future_pos[0], rook.future_pos[1])
                            rook.has_moved = True
                            self.setPos(self.future_pos[0], self.future_pos[1])
                            self.has_moved = True
                            self.chessboard.update_turn()
                        else:
                            self.setPos(self.future_pos[0], self.future_pos[1])
                            rook.setPos(rook.future_pos[0], rook.future_pos[1])
                elif self.future_pos[0] == self.current_pos[0] - 2 * self.square_size:  # castling to the left
                    if "rook0" in self.own_pieces.keys():
                        rook = self.chessboard.pieces[self.team]["rook0"]
                        if not self.check_for_checks(castling="left"):
                            rook.setPos(rook.future_pos[0], rook.future_pos[1])
                            rook.has_moved = True
                            self.setPos(self.future_pos[0], self.future_pos[1])
                            self.has_moved = True
                            self.chessboard.update_turn()
                        else:
                            self.setPos(self.future_pos[0], self.future_pos[1])
                            rook.setPos(rook.future_pos[0], rook.future_pos[1])
                else:  # "normal" move
                    if not self.check_for_checks():
                        self.setPos(self.future_pos[0], self.future_pos[1])
                        self.has_moved = True
                        self.chessboard.update_turn()
                    else:
                        self.setPos(self.future_pos[0], self.future_pos[1])
            else:  # pieces other than king
                if not self.check_for_checks():
                    self.setPos(self.future_pos[0], self.future_pos[1])
                    self.has_moved = True
                    self.chessboard.update_turn()
                else:
                    self.setPos(self.future_pos[0], self.future_pos[1])
        elif self.future_pos in self.possible_captures:  # capturing
            piece_for_capture = [p for p in list(self.opponent_pieces.values())
                                 if p.current_pos == self.future_pos][0]
            del self.opponent_pieces[piece_for_capture.chess_type]
            if not self.check_for_checks():
                self.chessboard.removeItem(piece_for_capture)
                self.setPos(self.future_pos[0], self.future_pos[1])
                self.has_moved = True
                self.chessboard.update_turn()
            else:
                self.opponent_pieces[piece_for_capture.chess_type] = piece_for_capture
                self.setPos(self.future_pos[0], self.future_pos[1])
        else:  # move not allowed
            self.future_pos = self.current_pos
            self.setPos(self.future_pos[0], self.future_pos[1])
            self.update_pos()

    def mate_or_draw(self):
        """Function that detects if there is a mate or a draw and calls appropriate function if there is one of them."""
        can_move = False
        moves = []
        captures = []
        chess_type = None
        for piece in list(self.own_pieces.values()):
            if can_move:
                break
            for move in piece.possible_moves:
                if can_move:
                    break
                piece.future_pos = move
                if not piece.check_for_checks(with_movement=False):
                    chess_type = piece.chess_type
                    moves.append(move)
                    can_move = True
            for capture in piece.possible_captures:
                if can_move:
                    break
                piece.future_pos = capture
                piece_for_capture = [p for p in list(self.opponent_pieces.values())
                                     if p.current_pos == piece.future_pos][0]
                del self.opponent_pieces[piece_for_capture.chess_type]
                if not piece.check_for_checks(with_movement=False):
                    chess_type = piece.chess_type
                    captures.append(capture)
                    can_move = True
                self.opponent_pieces[piece_for_capture.chess_type] = piece_for_capture
                piece.update_pos()


        print(self.team, chess_type, moves, captures)
        if not can_move and self.check:
            print("check mate")
            self.chessboard.game_over(result="check mate", winning_team=self.opponent_pieces["king"].team)
        elif not can_move and not self.check:
            print("draw")
            self.chessboard.game_over(result="draw")

    def init_update_pos(self, online=False, future_pos=None):
        """Function for updating position during the initialization of chessboard."""
        self.current_pos = self.x(), self.y()
        self.future_pos = self.current_pos

    def update_pos(self):
        """Function that updates possible moves for all pieces.
        Can be called once by any piece to update all the pieces on the board"""
        for team in list(self.chessboard.pieces.values()):
            for piece in list(team.values()):
                piece.update_possible_moves()

    def update_opponent_check(self):
        """Function that updates opponent's check."""
        opponent_check = False
        for piece in list(self.own_pieces.values()):
            for move in piece.possible_captures:
                if self.opponent_pieces["king"].current_pos == move:
                    opponent_check = True

        for piece in list(self.opponent_pieces.values()):
            piece.check = opponent_check

    def check_for_checks(self, castling=None, with_movement=True):
        """Function used for checking if there is a check after a move.
        Takes two arguments: castling = True if you want to check a castling move,
        with_movement = True if you want to check a move that is to be then performed.
        Returns "True" if a check is detected, otherwise returns False."""
        check = False

        if castling == "right":
            rook = self.chessboard.pieces[self.team]["rook1"]
            old_rook_pos = rook.current_pos
            rook.current_pos = rook.future_pos = (self.future_pos[0] - self.square_size, self.future_pos[1])
        elif castling == "left":
            rook = self.chessboard.pieces[self.team]["rook0"]
            old_rook_pos = rook.current_pos
            rook.current_pos = rook.future_pos = (self.future_pos[0] + self.square_size, self.future_pos[1])

        old_pos = self.current_pos
        self.current_pos = self.future_pos
        self.update_pos()

        for piece in list(self.opponent_pieces.values()):
            for move in piece.possible_captures:
                if self.own_pieces["king"].current_pos == move:
                    check = True
                if castling == "right" and not check:
                    if (self.own_pieces["king"].current_pos[0] - self.square_size,
                            self.own_pieces["king"].current_pos[1]) == move:
                        check = True
                if castling == "left" and not check:
                    if (self.own_pieces["king"].current_pos[0] + self.square_size,
                            self.own_pieces["king"].current_pos[1]) == move:
                        check = True

        if castling == "right" and not check:
            for piece in list(self.opponent_pieces.values()):
                for move in piece.possible_moves:
                    if (self.own_pieces["king"].current_pos[0] - 2 * self.square_size,
                            self.own_pieces["king"].current_pos[1]) == move:
                        check = True

        if castling == "left" and not check:
            for piece in list(self.opponent_pieces.values()):
                for move in piece.possible_moves:
                    if (self.own_pieces["king"].current_pos[0] + 2 * self.square_size,
                            self.own_pieces["king"].current_pos[1]) == move:
                        check = True

        if not check and with_movement:
            for piece in list(self.own_pieces.values()):
                piece.check = False
            self.update_opponent_check()
        elif check or not with_movement:
            self.future_pos = self.current_pos = old_pos
            if castling is not None:
                rook.future_pos = rook.current_pos = old_rook_pos
            self.update_pos()

        return check

    def update_possible_moves(self):
        """Function that updates possible moves of a given piece(self)."""
        direction = 1
        if self.team == "white":
            direction = -1
        elif self.team == "black":
            direction = 1
        match self.chess_type:
            case pawn if "pawn" in self.chess_type:
                (self.possible_moves,
                 self.possible_captures) = self.pawn_moves(direction)
            case rook if "rook" in self.chess_type:
                (self.possible_moves,
                 self.possible_captures) = self.rook_moves()
            case bishop if "bishop" in self.chess_type:
                (self.possible_moves,
                 self.possible_captures) = self.bishop_moves()
            case queen if "queen" in self.chess_type:
                (self.possible_moves,
                 self.possible_captures) = self.queen_moves()
            case knight if "knight" in self.chess_type:
                (self.possible_moves,
                 self.possible_captures) = self.knight_moves()
            case king if "king" in self.chess_type:
                (self.possible_moves,
                 self.possible_captures) = self.king_moves()

    def pawn_moves(self, direction):
        appr = True
        possible_moves = []
        possible_captures = []
        fut_pos = (self.current_pos[0], self.current_pos[1] + direction * self.square_size)
        if 0 <= fut_pos[1] <= 7 * self.square_size:
            for piece in list(self.own_pieces.values()):
                if piece.current_pos == fut_pos:
                    appr = False
            for piece in list(self.opponent_pieces.values()):
                if piece.current_pos == fut_pos:
                    appr = False
            if appr:
                possible_moves.append(fut_pos)
                fut_pos = (self.current_pos[0], self.current_pos[1] + direction * 2 * self.square_size)
                appr = True
                if fut_pos[1] <= 7 * self.square_size and not self.has_moved:
                    for piece in list(self.own_pieces.values()):
                        if piece.current_pos == fut_pos:
                            appr = False
                    for piece in list(self.opponent_pieces.values()):
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
                for piece in list(self.opponent_pieces.values()):
                    if piece.current_pos == position:
                        appr = True
                if appr:
                    possible_captures.append(position)
                    pass
        return possible_moves, possible_captures

    def knight_moves(self):
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
                for piece in list(self.own_pieces.values()):
                    if piece.current_pos == move:
                        appr = False
                if appr:
                    for piece in list(self.opponent_pieces.values()):
                        if piece.current_pos == move:
                            appr = False
                    if appr:
                        possible_moves.append(move)
                    else:
                        possible_captures.append(move)
        return possible_moves, possible_captures

    def rook_moves(self):
        appr = True
        possible_moves = []
        possible_captures = []
        num_moves = int((7 * self.square_size - self.current_pos[0]) / self.square_size)
        for i in range(num_moves):  # all the moves to the right side of a board
            fut_pos = (self.current_pos[0] + (i + 1) * self.square_size, self.current_pos[1])
            for piece in list(self.own_pieces.values()):
                if piece.current_pos == fut_pos:
                    appr = False
            if appr:
                for piece in list(self.opponent_pieces.values()):
                    if piece.current_pos == fut_pos:
                        possible_captures.append(fut_pos)
                        appr = False
                if appr:
                    possible_moves.append(fut_pos)
        num_moves = int((self.current_pos[0]) / self.square_size)
        appr = True
        for i in range(num_moves):  # all the moves to the left side of a board
            fut_pos = (self.current_pos[0] - (i + 1) * self.square_size, self.current_pos[1])
            for piece in list(self.own_pieces.values()):
                if piece.current_pos == fut_pos:
                    appr = False
            if appr:
                for piece in list(self.opponent_pieces.values()):
                    if piece.current_pos == fut_pos:
                        possible_captures.append(fut_pos)
                        appr = False
                if appr:
                    possible_moves.append(fut_pos)
        num_moves = int((7 * self.square_size - self.current_pos[1]) / self.square_size)
        appr = True
        for i in range(num_moves):  # all the moves to the bottom side of a board
            fut_pos = (self.current_pos[0], self.current_pos[1] + (i + 1) * self.square_size)
            for piece in list(self.own_pieces.values()):
                if piece.current_pos == fut_pos:
                    appr = False
            if appr:
                for piece in list(self.opponent_pieces.values()):
                    if piece.current_pos == fut_pos:
                        possible_captures.append(fut_pos)
                        appr = False
                if appr:
                    possible_moves.append(fut_pos)
        num_moves = int((self.current_pos[1]) / self.square_size)
        appr = True
        for i in range(num_moves):  # all the moves to the top side of a board
            fut_pos = (self.current_pos[0], self.current_pos[1] - (i + 1) * self.square_size)
            for piece in list(self.own_pieces.values()):
                if piece.current_pos == fut_pos:
                    appr = False
            if appr:
                for piece in list(self.opponent_pieces.values()):
                    if piece.current_pos == fut_pos:
                        possible_captures.append(fut_pos)
                        appr = False
                if appr:
                    possible_moves.append(fut_pos)
        return possible_moves, possible_captures

    def bishop_moves(self):
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
                    for piece in list(self.own_pieces.values()):
                        if piece.current_pos == fut_pos:
                            appr = False
                    if appr:
                        for piece in list(self.opponent_pieces.values()):
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
                    for piece in list(self.own_pieces.values()):
                        if piece.current_pos == fut_pos:
                            appr = False
                    if appr:
                        for piece in list(self.opponent_pieces.values()):
                            if piece.current_pos == fut_pos:
                                possible_captures.append(fut_pos)
                                appr = False
                        if appr:
                            possible_moves.append(fut_pos)
        return possible_moves, possible_captures

    def queen_moves(self):
        queen_moves = []
        queen_captures = []
        possible_moves = []
        possible_captures = []
        possible_moves, possible_captures = self.bishop_moves()
        queen_moves, queen_captures = self.rook_moves()
        for move in queen_moves:
            possible_moves.append(move)
        for capture in queen_captures:
            possible_captures.append(capture)
        return possible_moves, possible_captures

    def king_moves(self):
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
                for piece in list(self.own_pieces.values()):
                    if piece.current_pos == move:
                        appr = False
                if appr:
                    for piece in list(self.opponent_pieces.values()):
                        if piece.current_pos == move:
                            possible_captures.append(move)
                            appr = False
                    if appr:
                        possible_moves.append(move)
        for move in fut_pos_with_castling:  # move to the right, to the left and castling
            if (0 <= move[0] <= 7 * self.square_size
                    and 0 <= move[1] <= 7 * self.square_size):
                appr = True
                for piece in list(self.own_pieces.values()):
                    if piece.current_pos == move:
                        appr = False
                if appr:
                    for piece in list(self.opponent_pieces.values()):
                        if piece.current_pos == move:
                            possible_captures.append(move)
                            appr = False
                    if appr:
                        possible_moves.append(move)
                        appr = True
                        if not self.has_moved:  # castling
                            if move[0] - self.current_pos[0] > 0 and "rook1" in self.own_pieces.keys(): # castling to the right
                                if not self.own_pieces["rook1"].has_moved:
                                    move2 = (move[0] + self.square_size, move[1])
                                    for piece in list(self.own_pieces.values()):
                                        if piece.current_pos == move2:
                                            appr = False
                                    for piece in list(self.opponent_pieces.values()):
                                        if piece.current_pos == move2:
                                            appr = False
                                    if appr:
                                        possible_moves.append(move2)
                            elif move[0] - self.current_pos[0] < 0 and "rook0" in self.own_pieces.keys(): # castling to the left
                                if not self.own_pieces["rook0"].has_moved:
                                    fut_pos = [
                                        (move[0] - self.square_size, move[1]),
                                        (move[0] - 2 * self.square_size, move[1]),
                                    ]
                                    for move2 in fut_pos:
                                        for piece in list(self.own_pieces.values()):
                                            for piece in list(self.own_pieces.values()):
                                                if piece.current_pos == move2:
                                                    appr = False
                                        for piece in list(self.opponent_pieces.values()):
                                            for piece in list(self.opponent_pieces.values()):
                                                if piece.current_pos == move2:
                                                    appr = False
                                    if appr:
                                        possible_moves.append(fut_pos[0])
        return possible_moves, possible_captures
