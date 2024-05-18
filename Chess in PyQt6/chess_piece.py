from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QVBoxLayout, QPushButton, \
    QRadioButton, QWidget, QLineEdit
from PyQt6.QtGui import QPixmap, QPainter, QBrush, QColor, QPen, QPainterPath
from PyQt6.QtCore import QRectF

class ChessPiece(QGraphicsItem):
    szach_bialy = False
    szach_czarny = False

    def __init__(self, img_path, wielkosc_pola, typ, szachownica, parent=None, krol=None):
        super().__init__(parent)
        self.krol = krol
        self.wielkosc_pola = wielkosc_pola
        self.typ = typ
        self.szachownica = szachownica
        self.druzyna = None
        self.current_pos = self.x(), self.y()
        self.future_pos = self.current_pos
        self.has_moved = False

        self.img = QPixmap(img_path).scaled(self.wielkosc_pola, self.wielkosc_pola)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

    def boundingRect(self):
        bounds = self.wielkosc_pola
        return QRectF(0, 0, bounds, bounds)

    def shape(self):
        path = QPainterPath()
        bounds = self.wielkosc_pola
        path.addRect(0, 0, bounds - 20, bounds - 20)
        return path

    def paint(self, painter: QPainter, option, widget=None):
        painter.drawPixmap(0, 0, self.img)

    def mousePressEvent(self, event):
        if bool(self.flags() & QGraphicsItem.GraphicsItemFlag.ItemIsMovable):
            self.setScale(1.2)
        super().mousePressEvent(event)

    def update_pos(self, online=False, future_pos=None):
        if not online:
            self.current_pos = self.x(), self.y()
            self.future_pos = self.current_pos
            self.druzyna = "biale" if self == self.szachownica.biale[self.typ] else "czarne"
        else:
            if self.szachownica.tryb_gry == 2:
                self.future_pos = future_pos
                approval = self.can_move()
                # if approval[0]:
                if approval[1] is not None:
                    self.bicie(self.druzyna, approval[1])
                self.szachownica.zapis_ruchu(self)
                self.has_moved = True
                self.current_pos = self.future_pos
                self.setPos(self.future_pos[0], self.future_pos[1])
            if self.szachownica.tryb_gry == 3:
                self.future_pos = future_pos
                approval = self.can_move()
                # if approval[0]:
                if approval[1] is not None:
                    self.bicie(self.druzyna, approval[1])
                # self.szachownica.zapis_ruchu(self)
                self.has_moved = True
                self.current_pos = self.future_pos
                self.setPos(self.future_pos[0], self.future_pos[1])
                self.szachownica.update_turn()
        self.szachownica.refresh()

    def bicie(self, wlasne, pionek):
        if self.druzyna == "biale":
            cudze = self.szachownica.bierki["czarne"]
            if self.szachownica.tryb_gry == 3:
                del self.szachownica.komputer.czarne[pionek.typ]
        elif self.druzyna == "czarne":
            cudze = self.szachownica.bierki["biale"]
            if self.szachownica.tryb_gry == 3:
                del self.szachownica.komputer.biale[pionek.typ]
        index = list(cudze.keys())[list(cudze.values()).index(pionek)]
        self.szachownica.removeItem(pionek)
        del cudze[index]
        # print(len(cudze))

    #
    # def mouseMoveEvent(self, event):
    #     super().mouseMoveEvent(event)
    #

    def mouseReleaseEvent(self, event):
        self.setScale(1)
        x_round = round(self.x() / self.wielkosc_pola) * self.wielkosc_pola
        y_round = round(self.y() / self.wielkosc_pola) * self.wielkosc_pola
        self.future_pos = x_round, y_round
        if 0 <= self.future_pos[0] <= 7 * self.wielkosc_pola and 0 <= self.future_pos[1] <= 7 * self.wielkosc_pola:
            approval = self.can_move()
            if approval[0]:
                if approval[1] is not None:
                    self.bicie(self.druzyna, approval[1])
                self.szachownica.zapis_ruchu(self)
                self.szachownica.update_turn(self)
                self.has_moved = True
                self.current_pos = self.future_pos
                self.setPos(self.future_pos[0], self.future_pos[1])
                super().mouseReleaseEvent(event)
                if self.szachownica.tryb_gry == 3:
                    self.szachownica.ruch_komputera()
            else:
                self.future_pos = self.current_pos
                self.setPos(self.future_pos[0], self.future_pos[1])
                super().mouseReleaseEvent(event)
        else:
            self.future_pos = self.current_pos
            self.setPos(self.future_pos[0], self.future_pos[1])
            super().mouseReleaseEvent(event)


    def can_move(self):
        approval = False
        match self.typ:
            case pawn if "pawn" in self.typ:
                approval = self.pawn_positive()
            case knight if "knight" in self.typ:
                approval = self.knight_positive()
            case bishop if "bishop" in self.typ:
                approval = self.bishop_positive()
            case queen if "queen" in self.typ:
                approval = self.queen_positive()
            case rook if "rook" in self.typ:
                approval = self.rook_positive()
            case king if "king" in self.typ:
                approval = self.king_positive()
        return approval

    def pawn_positive(self):
        appr = True
        pion_do_bicia = None
        biale = self.szachownica.bierki["biale"]
        czarne = self.szachownica.bierki["czarne"]
        if self in list(czarne.values()):
            i = 1
        else:
            i = -1
        if self.future_pos[1] == self.current_pos[1] + i * self.wielkosc_pola:  # ruch o jedno pole
            if self.future_pos[0] == self.current_pos[0]:  # ruch o jedno pole do przodu
                for pionek in list(czarne.values()):
                    if pionek.current_pos == self.future_pos:
                        appr = False
                for pionek in list(biale.values()):
                    if pionek.current_pos == self.future_pos:
                        appr = False
            elif self.future_pos[0] == self.current_pos[0] + self.wielkosc_pola or self.future_pos[0] == \
                    self.current_pos[0] - self.wielkosc_pola:  # ruch na skos
                if i == 1:  # czarny pion
                    appr = False
                    for pionek in list(czarne.values()):
                        if pionek.current_pos == self.future_pos:
                            appr = False
                    for pionek in list(biale.values()):
                        if pionek.current_pos == self.future_pos:
                            pion_do_bicia = pionek
                            appr = True
                            # self.bicie(biale, pionek)
                else:  # bialy pion
                    appr = False
                    for pionek in list(biale.values()):
                        if pionek.current_pos == self.future_pos:
                            appr = False
                    for pionek in list(czarne.values()):
                        if pionek.current_pos == self.future_pos:
                            pion_do_bicia = pionek
                            appr = True
                            # self.bicie(czarne, pionek)
        elif (self.future_pos[1] == self.current_pos[1] + 2 * i * self.wielkosc_pola
              and not self.has_moved):  # ruch o dwa pola co przodu
            if self.future_pos[0] == self.current_pos[0]:
                for piece in list(biale.values()):
                    if (self.future_pos == piece.current_pos or
                            (self.future_pos[0], self.future_pos[1] - i * self.wielkosc_pola) == piece.current_pos):
                        appr = False
                for piece in list(czarne.values()):
                    if (self.future_pos == piece.current_pos or
                            (self.future_pos[0], self.future_pos[1] - i * self.wielkosc_pola) == piece.current_pos):
                        appr = False
            else:
                appr = False
        else:
            appr = False
        return appr, pion_do_bicia

    def knight_positive(self):
        appr = True
        pion_do_bicia = None
        biale = self.szachownica.bierki["biale"]
        czarne = self.szachownica.bierki["czarne"]
        if self in list(czarne.values()):
            i = 1
        else:
            i = -1
        if (self.future_pos[0] == self.current_pos[0] + 2 * self.wielkosc_pola
                or self.future_pos[0] == self.current_pos[0] - 2 * self.wielkosc_pola):
            if (self.future_pos[1] == self.current_pos[1] + self.wielkosc_pola
                    or self.future_pos[1] == self.current_pos[1] - self.wielkosc_pola):
                if i == 1:  # czarny
                    for pionek in list(czarne.values()):
                        if pionek.current_pos == self.future_pos:
                            appr = False
                    for pionek in list(biale.values()):
                        if pionek.current_pos == self.future_pos:
                            pion_do_bicia = pionek
                            # self.bicie(biale, pionek)
                else:  # bialy
                    for pionek in list(biale.values()):
                        if pionek.current_pos == self.future_pos:
                            appr = False
                    for pionek in list(czarne.values()):
                        if pionek.current_pos == self.future_pos:
                            pion_do_bicia = pionek
                            # self.bicie(czarne, pionek)
            else:
                appr = False
        elif (self.future_pos[0] == self.current_pos[0] + self.wielkosc_pola
              or self.future_pos[0] == self.current_pos[0] - self.wielkosc_pola):
            if (self.future_pos[1] == self.current_pos[1] + 2 * self.wielkosc_pola
                    or self.future_pos[1] == self.current_pos[1] - 2 * self.wielkosc_pola):
                if i == 1:  # czarny
                    for pionek in list(czarne.values()):
                        if pionek.current_pos == self.future_pos:
                            appr = False
                    for pionek in list(biale.values()):
                        if pionek.current_pos == self.future_pos:
                            pion_do_bicia = pionek
                            # self.bicie(biale, pionek)
                else:  # bialy
                    for pionek in list(biale.values()):
                        if pionek.current_pos == self.future_pos:
                            appr = False
                    for pionek in list(czarne.values()):
                        if pionek.current_pos == self.future_pos:
                            pion_do_bicia = pionek
                            # self.bicie(czarne, pionek)
            else:
                appr = False
        else:
            appr = False
        return appr, pion_do_bicia

    def bishop_positive(self):
        appr = True
        biale = self.szachownica.bierki["biale"]
        czarne = self.szachownica.bierki["czarne"]
        pion_do_bicia = None
        if self in list(czarne.values()):
            i = 1
        else:
            i = -1
        if abs(self.future_pos[0] - self.current_pos[0]) == abs(self.future_pos[1] - self.current_pos[1]) != 0:
            ilosc_pol = int(abs(self.future_pos[0] - self.current_pos[0]) / self.wielkosc_pola)
            znak_x = 1 if self.future_pos[0] - self.current_pos[0] > 0 else -1
            znak_y = 1 if self.future_pos[1] - self.current_pos[1] > 0 else -1
            if i == 1:  # czarny
                for j in range(ilosc_pol):
                    for pionek_czarny in list(czarne.values()):
                        if (pionek_czarny.current_pos == (self.current_pos[0] + znak_x * (j + 1) * self.wielkosc_pola,
                                                          self.current_pos[1] + znak_y * (j + 1) * self.wielkosc_pola)
                                and pionek_czarny != self):
                            appr = False
                if appr is True:
                    for j in range(ilosc_pol):
                        for pionek_bialy in list(biale.values()):
                            if pionek_bialy.current_pos == (self.current_pos[0] + znak_x * j * self.wielkosc_pola,
                                                            self.current_pos[1] + znak_y * j * self.wielkosc_pola):
                                appr = False
                                pion_do_bicia = None
                            else:
                                if pionek_bialy.current_pos == self.future_pos:
                                    pion_do_bicia = pionek_bialy
                if appr is True and pion_do_bicia is not None:
                    pass
                    # self.bicie(biale, pion_do_bicia)
            else:  # bialy
                for j in range(ilosc_pol):
                    for pionek_bialy in list(biale.values()):
                        if (pionek_bialy.current_pos == (self.current_pos[0] + znak_x * (j + 1) * self.wielkosc_pola,
                                                         self.current_pos[1] + znak_y * (j + 1) * self.wielkosc_pola)
                                and pionek_bialy != self):
                            appr = False
                if appr is True:
                    for j in range(ilosc_pol):
                        for pionek_bialy in list(czarne.values()):
                            if pionek_bialy.current_pos == (self.current_pos[0] + znak_x * j * self.wielkosc_pola,
                                                            self.current_pos[1] + znak_y * j * self.wielkosc_pola):
                                appr = False
                                pion_do_bicia = None
                            else:
                                if pionek_bialy.current_pos == self.future_pos:
                                    pion_do_bicia = pionek_bialy
                if appr is True and pion_do_bicia is not None:
                    pass
                    # self.bicie(czarne, pion_do_bicia)

        else:
            appr = False
        return appr, pion_do_bicia

    def rook_positive(self):
        appr = True
        biale = self.szachownica.bierki["biale"]
        czarne = self.szachownica.bierki["czarne"]
        pion_do_bicia = None
        if self in list(czarne.values()):
            i = 1
        else:
            i = -1
        if self.future_pos[0] != self.current_pos[0] and self.future_pos[1] == self.current_pos[1]:  # poziom
            ilosc_pol = int(abs(self.future_pos[0] - self.current_pos[0]) / self.wielkosc_pola)
            znak = 1 if self.future_pos[0] - self.current_pos[0] > 0 else -1
            if i == 1:  # czarny
                for j in range(ilosc_pol):
                    for pionek_czarny in list(czarne.values()):
                        if (pionek_czarny.current_pos == (
                                self.current_pos[0] + znak * (j + 1) * self.wielkosc_pola, self.current_pos[1])
                                and pionek_czarny != self):
                            appr = False
                if appr is True:
                    for j in range(ilosc_pol):
                        for pionek_bialy in list(biale.values()):
                            if pionek_bialy.current_pos == (
                                    self.current_pos[0] + znak * j * self.wielkosc_pola, self.current_pos[1]):
                                appr = False
                                pion_do_bicia = None
                            else:
                                if pionek_bialy.current_pos == self.future_pos:
                                    pion_do_bicia = pionek_bialy
                if appr is True and pion_do_bicia is not None:
                    pass
                    # self.bicie(biale, pion_do_bicia)
            else:  # bialy
                for j in range(ilosc_pol):
                    for pionek_bialy in list(biale.values()):
                        if (pionek_bialy.current_pos ==
                                (self.current_pos[0] + znak * (j + 1) * self.wielkosc_pola, self.future_pos[1])
                                and pionek_bialy != self):
                            appr = False
                if appr is True:
                    for j in range(ilosc_pol):
                        for pionek_czarny in list(czarne.values()):
                            if (pionek_czarny.current_pos ==
                                    (self.current_pos[0] + znak * j * self.wielkosc_pola, self.future_pos[1])):
                                appr = False
                                pion_do_bicia = None
                            else:
                                if pionek_czarny.current_pos == self.future_pos:
                                    pion_do_bicia = pionek_czarny
                if appr is True and pion_do_bicia is not None:
                    pass
                    # self.bicie(czarne, pion_do_bicia)
        elif self.future_pos[0] == self.current_pos[0] and self.future_pos[1] != self.current_pos[1]:  # pion
            ilosc_pol = int(abs(self.future_pos[1] - self.current_pos[1]) / self.wielkosc_pola)
            znak = 1 if self.future_pos[1] - self.current_pos[1] > 0 else -1
            if i == 1:  # czarny
                for j in range(ilosc_pol):
                    for pionek_czarny in list(czarne.values()):
                        if (pionek_czarny.current_pos == (
                                self.current_pos[0], self.current_pos[1] + znak * (j + 1) * self.wielkosc_pola)
                                and pionek_czarny != self):
                            appr = False
                if appr is True:
                    for j in range(ilosc_pol):
                        for pionek_bialy in list(biale.values()):
                            if pionek_bialy.current_pos == (
                                    self.current_pos[0], self.current_pos[1] + znak * j * self.wielkosc_pola):
                                appr = False
                                pion_do_bicia = None
                            else:
                                if pionek_bialy.current_pos == self.future_pos:
                                    pion_do_bicia = pionek_bialy
                if appr is True and pion_do_bicia is not None:
                    pass
                    # self.bicie(biale, pion_do_bicia)
            else:  # bialy
                for j in range(ilosc_pol):
                    for pionek_bialy in list(biale.values()):
                        if (pionek_bialy.current_pos == (
                                self.current_pos[0], self.current_pos[1] + znak * (j + 1) * self.wielkosc_pola)
                                and pionek_bialy != self):
                            appr = False
                if appr is True:
                    for j in range(ilosc_pol):
                        for pionek_czarny in list(czarne.values()):
                            if (pionek_czarny.current_pos ==
                                    (self.current_pos[0], self.current_pos[1] + znak * j * self.wielkosc_pola)):
                                appr = False
                                pion_do_bicia = None
                            else:
                                if pionek_czarny.current_pos == self.future_pos:
                                    pion_do_bicia = pionek_czarny
                if appr is True and pion_do_bicia is not None:
                    pass
                    # self.bicie(czarne, pion_do_bicia)
        else:
            appr = False
        return appr, pion_do_bicia

    def queen_positive(self):
        appr = True
        if (self.future_pos[0] != self.current_pos[0] and self.future_pos[1] == self.current_pos[1]) \
                or (self.future_pos[0] == self.current_pos[0] and self.future_pos[1] != self.current_pos[1]):
            appr = self.rook_positive()
        elif abs(self.future_pos[0] - self.current_pos[0]) == abs(self.future_pos[1] - self.current_pos[1]) != 0:
            appr = self.bishop_positive()
        else:
            appr = False, None
        return appr

    def king_positive(self):
        appr = True
        biale = self.szachownica.bierki["biale"]
        czarne = self.szachownica.bierki["czarne"]
        pion_do_bicia = None
        if self in list(czarne.values()):
            i = 1
        else:
            i = -1
        if abs(self.future_pos[0] - self.current_pos[0]) == abs(self.future_pos[1] - self.current_pos[1]):
            if i == 1:  # czarne
                for pionek_czarny in list(czarne.values()):
                    if pionek_czarny.current_pos == self.future_pos:
                        appr = False
                if appr is True:
                    for pionek_bialy in list(biale.values()):
                        if pionek_bialy.current_pos == self.future_pos:
                            pion_do_bicia = pionek_bialy
                if appr is True and pion_do_bicia is not None:
                    pass
                    # self.bicie(biale, pion_do_bicia)
            else:
                for pionek_bialy in list(biale.values()):
                    if pionek_bialy.current_pos == self.future_pos:
                        appr = False
                if appr is True:  # biale
                    for pionek_czarny in list(czarne.values()):
                        if pionek_czarny.current_pos == self.future_pos:
                            pion_do_bicia = pionek_czarny
                if appr is True and pion_do_bicia is not None:
                    pass
                    # self.bicie(czarne, pion_do_bicia)
        elif self.future_pos[0] == self.current_pos[0] and abs(
                self.future_pos[1] - self.current_pos[1]) == self.wielkosc_pola:  # pion
            if i == 1:  # czarne
                for pionek_czarny in list(czarne.values()):
                    if pionek_czarny.current_pos == self.future_pos:
                        appr = False
                if appr is True:
                    for pionek_bialy in list(biale.values()):
                        if pionek_bialy.current_pos == self.future_pos:
                            pion_do_bicia = pionek_bialy
                if appr is True and pion_do_bicia is not None:
                    pass
                    # self.bicie(biale, pion_do_bicia)
            else:
                for pionek_bialy in list(biale.values()):
                    if pionek_bialy.current_pos == self.future_pos:
                        appr = False
                if appr is True:  # biale
                    for pionek_czarny in list(czarne.values()):
                        if pionek_czarny.current_pos == self.future_pos:
                            pion_do_bicia = pionek_czarny
                if appr is True and pion_do_bicia is not None:
                    pass
                    # self.bicie(czarne, pion_do_bicia)
        elif self.future_pos[0] != self.current_pos[0] and self.future_pos[1] == self.current_pos[1]:  # poziom
            if abs(self.future_pos[0] - self.current_pos[0]) == self.wielkosc_pola:
                if i == 1:  # czarne
                    for pionek_czarny in list(czarne.values()):
                        if pionek_czarny.current_pos == self.future_pos:
                            appr = False
                    if appr is True:
                        for pionek_bialy in list(biale.values()):
                            if pionek_bialy.current_pos == self.future_pos:
                                pion_do_bicia = pionek_bialy
                    if appr is True and pion_do_bicia is not None:
                        pass
                        # self.bicie(biale, pion_do_bicia)
                else:
                    for pionek_bialy in list(biale.values()):
                        if pionek_bialy.current_pos == self.future_pos:
                            appr = False
                    if appr is True:  # biale
                        for pionek_czarny in list(czarne.values()):
                            if pionek_czarny.current_pos == self.future_pos:
                                pion_do_bicia = pionek_czarny
                    if appr is True and pion_do_bicia is not None:
                        pass
                        # self.bicie(czarne, pion_do_bicia)
            else:
                appr = False

        else:
            appr = False
        return appr, pion_do_bicia

    def szach(self, druzyna):
        szach = False
        biale = self.szachownica.bierki["biale"]
        czarne = self.szachownica.bierki["czarne"]
        if druzyna == "czarne":
            swoje = czarne
            cudze = biale
        else:
            cudze = czarne
            swoje = biale

        for piece in list(cudze.values()):
            pos = piece.future_pos
            piece.future_pos = self.krol.current_pos
            if piece.can_move():
                szach = True
            piece.future_pos = pos

        return szach