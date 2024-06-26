from PyQt6.QtWidgets import QGraphicsScene, QGraphicsItem
from PyQt6.QtGui import QBrush, QColor, QPen
from chess_piece import ChessPiece


class Chessboard(QGraphicsScene):
    def __init__(self, square_size, main_window):
        super().__init__()
        self.square_size = square_size
        self.main_window = main_window
        self.pieces = {}
        self.white = {}
        self.black = {}
        self.turn = "white"
        self.initUI()

    def initUI(self):  # initialization of a chessboard
        self.draw_board()
        self.draw_pieces()

    def draw_board(self):  # drawing board
        self.setSceneRect(0, 0, self.square_size * 8, self.square_size * 8)
        for row in range(8):
            for col in range(8):
                x = col * self.square_size
                y = row * self.square_size
                if (row + col) % 2 == 0:
                    color = QColor("brown")
                else:
                    color = QColor("beige")
                self.addRect(x, y, self.square_size, self.square_size, QPen(QColor("black")), QBrush(color))

    def draw_pieces(self):  # creating chess pieces
        length = width = self.square_size * 7

        piece = ChessPiece(img_path="Chess_pieces_pngs/white_king.png", square_size=self.square_size,
                           chess_type=f"king", chessboard=self)
        piece.setPos(width - 3 * self.square_size, length)
        self.addItem(piece)

        piece = ChessPiece(img_path="Chess_pieces_pngs/black_king.png", square_size=self.square_size,
                           chess_type=f"king", chessboard=self)
        piece.setPos(width - 3 * self.square_size, 0)
        self.addItem(piece)

        for j in range(2):
            piece = ChessPiece(img_path="Chess_pieces_pngs/white_rook.png", square_size=self.square_size,
                               chess_type=f"rook{j}", chessboard=self)
            piece.setPos(j * width, length)
            self.addItem(piece)

            piece = ChessPiece(img_path="Chess_pieces_pngs/black_rook.png", square_size=self.square_size,
                               chess_type=f"rook{j}", chessboard=self)
            piece.setPos(j * width, 0)
            self.addItem(piece)

        for j in range(2):
            offset = 1 if j % 2 == 0 else -1
            piece = ChessPiece(img_path="Chess_pieces_pngs/white_knight.png", square_size=self.square_size,
                               chess_type=f"knight{j}", chessboard=self)
            piece.setPos(j * width + offset * self.square_size, length)
            self.addItem(piece)

            piece = ChessPiece(img_path="Chess_pieces_pngs/black_knight.png", square_size=self.square_size,
                               chess_type=f"knight{j}", chessboard=self)
            piece.setPos(j * width + offset * self.square_size, 0)
            self.addItem(piece)

        for j in range(2):
            offset = 2 if j % 2 == 0 else -2
            piece = ChessPiece(img_path="Chess_pieces_pngs/white_bishop.png", square_size=self.square_size,
                               chess_type=f"bishop{j}", chessboard=self)
            piece.setPos(j * width + offset * self.square_size, length)
            self.addItem(piece)

            piece = ChessPiece(img_path="Chess_pieces_pngs/black_bishop.png", square_size=self.square_size,
                               chess_type=f"bishop{j}", chessboard=self)
            piece.setPos(j * width + offset * self.square_size, 0)
            self.addItem(piece)

        piece = ChessPiece(img_path="Chess_pieces_pngs/white_queen.png", square_size=self.square_size,
                           chess_type=f"queen", chessboard=self)
        piece.setPos(3 * self.square_size, length)
        self.addItem(piece)

        piece = ChessPiece(img_path="Chess_pieces_pngs/black_queen.png", square_size=self.square_size,
                           chess_type=f"queen", chessboard=self)
        piece.setPos(3 * self.square_size, 0)
        self.addItem(piece)

        pawns = ["Chess_pieces_pngs/white_pawn.png", "Chess_pieces_pngs/black_pawn.png"]
        for i in range(8):
            for j, path in enumerate(pawns):
                piece = ChessPiece(img_path=path, square_size=self.square_size,
                                   chess_type=f"pawn{i}", chessboard=self)
                if j % 2 == 0:
                    y = (length - self.square_size)
                else:
                    y = self.square_size
                x = self.square_size * i
                piece.setPos(x, y)
                self.addItem(piece)

        for piece in self.items():
            if isinstance(piece, ChessPiece):
                piece.init_update_pos()
                if piece.y() < length/2:
                    self.black[piece.chess_type] = piece
                    piece.team = "black"
                    piece.own_pieces = self.black
                    piece.opponent_pieces = self.white
                    piece.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
                else:
                    self.white[piece.chess_type] = piece
                    piece.team = "white"
                    piece.own_pieces = self.white
                    piece.opponent_pieces = self.black
                    piece.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.pieces["white"] = self.white
        self.pieces["black"] = self.black
        self.white["king"].update_pos()

    def update_turn(self):  # function for changing turns
        if self.turn == "white":
            self.turn = "black"
            for piece in list(self.white.values()):
                piece.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
            for piece in list(self.black.values()):
                piece.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            self.black["king"].update_pos()
            self.black["king"].mate_or_draw()
        elif self.turn == "black":
            self.turn = "white"
            for piece in list(self.white.values()):
                piece.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            for piece in list(self.black.values()):
                piece.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
            self.white["king"].update_pos()
            self.white["king"].mate_or_draw()

    def game_over(self, result, winning_team=None):
        for piece in list(self.white.values()):
            piece.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        for piece in list(self.black.values()):
            piece.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.main_window.show_end_game_window(result, winning_team)




