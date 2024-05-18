from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QVBoxLayout, QPushButton, \
    QRadioButton, QWidget, QLineEdit
from PyQt6.QtGui import QPixmap, QPainter, QBrush, QColor, QPen, QPainterPath
from PyQt6.QtCore import QRectF
import random

class AI:
    def __init__(self, biale, czarne, wielkosc_pola):
        self.biale = {piece.typ: [piece, 0, [], []] for piece in list(biale.values())}
        self.czarne = {piece.typ: [piece, 0, [], []] for piece in list(czarne.values())}
        self.wielkosc_pola = wielkosc_pola
        self.obliczanie_wartosci_poczatkowej()
        self.mozliwe_ruchy()

    def obliczanie_wartosci_poczatkowej(self):
        for key, piece in self.biale.items():
            if "pawn" in key:
                piece[1] = -1
            elif "knight" in key or "bishop" in key:
                piece[1] = -3
            elif "queen" in key:
                piece[1] = -9
            elif "rook" in key:
                piece[1] = -5
        for key, piece in self.czarne.items():
            if "pawn" in key:
                piece[1] = 1
            elif "knight" in key or "bishop" in key:
                piece[1] = 3
            elif "queen" in key:
                piece[1] = 9
            elif "rook" in key:
                piece[1] = 5

    def mozliwe_ruchy(self):
        for i in range(2):
            if i == 0:
                wlasne = self.czarne
                cudze = self.biale
                l = 1
            elif i == 1:
                wlasne = self.biale
                cudze = self.czarne
                l = -1
            for key, piece_info in wlasne.items():
                ruchy = []
                appr = True
                if "pawn" in key:
                    ruchy, bicie = self.pawn_moves(piece_info[0])
                    piece_info[2] = ruchy
                    piece_info[3] = bicie
                if "rook" in key:
                    appr = True
                    liczba_ruchow = int((7 * self.wielkosc_pola - piece_info[0].current_pos[1]) / self.wielkosc_pola)
                    for i in range(liczba_ruchow):
                        fut_pos = (piece_info[0].current_pos[0], piece_info[0].current_pos[1] + (i+1) * self.wielkosc_pola)
                        for klucz, pionek in wlasne.items():
                            if pionek[0].current_pos == fut_pos:
                                appr = False
                        if appr:
                            for klucz, pionek in cudze.items():
                                if pionek[0].current_pos == fut_pos:
                                    ruchy.append(fut_pos)
                                    appr = False
                        if appr:
                            ruchy.append(fut_pos)
                    appr = True
                    liczba_ruchow = int(piece_info[0].current_pos[1] / self.wielkosc_pola)
                    for i in range(liczba_ruchow):
                        fut_pos = (piece_info[0].current_pos[0], piece_info[0].current_pos[1] - (i + 1) * self.wielkosc_pola)
                        for klucz, pionek in wlasne.items():
                            if pionek[0].current_pos == fut_pos:
                                appr = False
                        if appr:
                            for klucz, pionek in cudze.items():
                                if pionek[0].current_pos == fut_pos:
                                    ruchy.append(fut_pos)
                                    appr = False
                        if appr:
                            ruchy.append(fut_pos)
                    appr = True
                    liczba_ruchow = int((7 * self.wielkosc_pola - piece_info[0].current_pos[0]) / self.wielkosc_pola)
                    for i in range(liczba_ruchow):
                        fut_pos = (piece_info[0].current_pos[0] + (i + 1) * self.wielkosc_pola, piece_info[0].current_pos[1])
                        for klucz, pionek in wlasne.items():
                            if pionek[0].current_pos == fut_pos:
                                appr = False
                        if appr:
                            for klucz, pionek in cudze.items():
                                if pionek[0].current_pos == fut_pos:
                                    ruchy.append(fut_pos)
                                    appr = False
                        if appr:
                            ruchy.append(fut_pos)
                    appr = True
                    liczba_ruchow = int(piece_info[0].current_pos[0] / self.wielkosc_pola)
                    for i in range(liczba_ruchow):
                        fut_pos = (piece_info[0].current_pos[0] - (i + 1) * self.wielkosc_pola, piece_info[0].current_pos[1])
                        for klucz, pionek in wlasne.items():
                            if pionek[0].current_pos == fut_pos:
                                appr = False
                        if appr:
                            for klucz, pionek in cudze.items():
                                if pionek[0].current_pos == fut_pos:
                                    ruchy.append(fut_pos)
                                    appr = False
                        if appr:
                            ruchy.append(fut_pos)
                if "bishop" in key:
                    appr = True
                    prawa_sciana = int((7 * self.wielkosc_pola - piece_info[0].current_pos[0]) / self.wielkosc_pola)
                    lewa_sciana = int(piece_info[0].current_pos[0] / self.wielkosc_pola)
                    for i in range(prawa_sciana):
                        fut_pos = (piece_info[0].current_pos[0] + (i+1)*self.wielkosc_pola,
                                   piece_info[0].current_pos[1] - (i+1)*self.wielkosc_pola)
                        if 0 <= fut_pos[0] <= 7 * self.wielkosc_pola and 0 <= fut_pos[1] <= 7 * self.wielkosc_pola:
                            for klucz, pionek in wlasne.items():
                                if pionek[0].current_pos == fut_pos:
                                    appr = False
                            if appr:
                                for klucz, pionek in cudze.items():
                                    if pionek[0].current_pos == fut_pos:
                                        ruchy.append(fut_pos)
                                        appr = False
                            if appr:
                                ruchy.append(fut_pos)
                    appr = True
                    for i in range(prawa_sciana):
                        fut_pos = (piece_info[0].current_pos[0] + (i + 1) * self.wielkosc_pola,
                                   piece_info[0].current_pos[1] + (i + 1) * self.wielkosc_pola)
                        if 0 <= fut_pos[0] <= 7 * self.wielkosc_pola and 0 <= fut_pos[1] <= 7 * self.wielkosc_pola:
                            for klucz, pionek in wlasne.items():
                                if pionek[0].current_pos == fut_pos:
                                    appr = False
                            if appr:
                                for klucz, pionek in cudze.items():
                                    if pionek[0].current_pos == fut_pos:
                                        ruchy.append(fut_pos)
                                        appr = False
                            if appr:
                                ruchy.append(fut_pos)
                    appr = True
                    for i in range(lewa_sciana):
                        fut_pos = (piece_info[0].current_pos[0] - (i+1)*self.wielkosc_pola,
                                   piece_info[0].current_pos[1] - (i+1)*self.wielkosc_pola)
                        if 0 <= fut_pos[0] <= 7 * self.wielkosc_pola and 0 <= fut_pos[1] <= 7 * self.wielkosc_pola:
                            for klucz, pionek in wlasne.items():
                                if pionek[0].current_pos == fut_pos:
                                    appr = False
                            if appr:
                                for klucz, pionek in cudze.items():
                                    if pionek[0].current_pos == fut_pos:
                                        ruchy.append(fut_pos)
                                        appr = False
                            if appr:
                                ruchy.append(fut_pos)
                    appr = True
                    for i in range(lewa_sciana):
                        fut_pos = (piece_info[0].current_pos[0] - (i+1)*self.wielkosc_pola,
                                   piece_info[0].current_pos[1] + (i+1)*self.wielkosc_pola)
                        if 0 <= fut_pos[0] <= 7 * self.wielkosc_pola and 0 <= fut_pos[1] <= 7 * self.wielkosc_pola:
                            for klucz, pionek in wlasne.items():
                                if pionek[0].current_pos == fut_pos:
                                    appr = False
                            if appr:
                                for klucz, pionek in cudze.items():
                                    if pionek[0].current_pos == fut_pos:
                                        ruchy.append(fut_pos)
                                        appr = False
                            if appr:
                                ruchy.append(fut_pos)
                if "knight" in key:
                    appr = True
                    fut_pos = (piece_info[0].current_pos[0] + 2*self.wielkosc_pola,
                               piece_info[0].current_pos[1] + self.wielkosc_pola)
                    if 0 <= fut_pos[0] <= 7 * self.wielkosc_pola and 0 <= fut_pos[1] <= 7 * self.wielkosc_pola:
                        for klucz, pionek in wlasne.items():
                            if pionek[0].current_pos == fut_pos:
                                appr = False
                        for klucz, pionek in cudze.items():
                            if pionek[0].current_pos == fut_pos:
                                ruchy.append(fut_pos)
                                appr = False
                        if appr:
                            ruchy.append(fut_pos)
                    appr = True
                    fut_pos = (piece_info[0].current_pos[0] + 2 * self.wielkosc_pola,
                               piece_info[0].current_pos[1] - self.wielkosc_pola)
                    if 0 <= fut_pos[0] <= 7 * self.wielkosc_pola and 0 <= fut_pos[1] <= 7 * self.wielkosc_pola:
                        for klucz, pionek in wlasne.items():
                            if pionek[0].current_pos == fut_pos:
                                appr = False
                        for klucz, pionek in cudze.items():
                            if pionek[0].current_pos == fut_pos:
                                ruchy.append(fut_pos)
                                appr = False
                        if appr:
                            ruchy.append(fut_pos)
                    appr = True
                    fut_pos = (piece_info[0].current_pos[0] - 2 * self.wielkosc_pola,
                               piece_info[0].current_pos[1] - self.wielkosc_pola)
                    if 0 <= fut_pos[0] <= 7 * self.wielkosc_pola and 0 <= fut_pos[1] <= 7 * self.wielkosc_pola:
                        for klucz, pionek in wlasne.items():
                            if pionek[0].current_pos == fut_pos:
                                appr = False
                        for klucz, pionek in cudze.items():
                            if pionek[0].current_pos == fut_pos:
                                ruchy.append(fut_pos)
                                appr = False
                        if appr:
                            ruchy.append(fut_pos)
                    appr = True
                    fut_pos = (piece_info[0].current_pos[0] - 2 * self.wielkosc_pola,
                               piece_info[0].current_pos[1] + self.wielkosc_pola)
                    if 0 <= fut_pos[0] <= 7 * self.wielkosc_pola and 0 <= fut_pos[1] <= 7 * self.wielkosc_pola:
                        for klucz, pionek in wlasne.items():
                            if pionek[0].current_pos == fut_pos:
                                appr = False
                        for klucz, pionek in cudze.items():
                            if pionek[0].current_pos == fut_pos:
                                ruchy.append(fut_pos)
                                appr = False
                        if appr:
                            ruchy.append(fut_pos)

                    appr = True
                    fut_pos = (piece_info[0].current_pos[0] + self.wielkosc_pola,
                               piece_info[0].current_pos[1] + 2*self.wielkosc_pola)
                    if 0 <= fut_pos[0] <= 7 * self.wielkosc_pola and 0 <= fut_pos[1] <= 7 * self.wielkosc_pola:
                        for klucz, pionek in wlasne.items():
                            if pionek[0].current_pos == fut_pos:
                                appr = False
                        for klucz, pionek in cudze.items():
                            if pionek[0].current_pos == fut_pos:
                                ruchy.append(fut_pos)
                                appr = False
                        if appr:
                            ruchy.append(fut_pos)
                    appr = True
                    fut_pos = (piece_info[0].current_pos[0] + self.wielkosc_pola,
                               piece_info[0].current_pos[1] - 2*self.wielkosc_pola)
                    if 0 <= fut_pos[0] <= 7 * self.wielkosc_pola and 0 <= fut_pos[1] <= 7 * self.wielkosc_pola:
                        for klucz, pionek in wlasne.items():
                            if pionek[0].current_pos == fut_pos:
                                appr = False
                        for klucz, pionek in cudze.items():
                            if pionek[0].current_pos == fut_pos:
                                ruchy.append(fut_pos)
                                appr = False
                        if appr:
                            ruchy.append(fut_pos)
                    appr = True
                    fut_pos = (piece_info[0].current_pos[0] - self.wielkosc_pola,
                               piece_info[0].current_pos[1] - 2*self.wielkosc_pola)
                    if 0 <= fut_pos[0] <= 7 * self.wielkosc_pola and 0 <= fut_pos[1] <= 7 * self.wielkosc_pola:
                        for klucz, pionek in wlasne.items():
                            if pionek[0].current_pos == fut_pos:
                                appr = False
                        for klucz, pionek in cudze.items():
                            if pionek[0].current_pos == fut_pos:
                                ruchy.append(fut_pos)
                                appr = False
                        if appr:
                            ruchy.append(fut_pos)
                    appr = True
                    fut_pos = (piece_info[0].current_pos[0] - self.wielkosc_pola,
                               piece_info[0].current_pos[1] + 2*self.wielkosc_pola)
                    if 0 <= fut_pos[0] <= 7 * self.wielkosc_pola and 0 <= fut_pos[1] <= 7 * self.wielkosc_pola:
                        for klucz, pionek in wlasne.items():
                            if pionek[0].current_pos == fut_pos:
                                appr = False
                        for klucz, pionek in cudze.items():
                            if pionek[0].current_pos == fut_pos:
                                ruchy.append(fut_pos)
                                appr = False
                        if appr:
                            ruchy.append(fut_pos)
                if "queen" in key:
                    appr = True
                    prawa_sciana = int((7 * self.wielkosc_pola - piece_info[0].current_pos[0]) / self.wielkosc_pola)
                    lewa_sciana = int(piece_info[0].current_pos[0] / self.wielkosc_pola)
                    for i in range(prawa_sciana):
                        fut_pos = (piece_info[0].current_pos[0] + (i + 1) * self.wielkosc_pola,
                                   piece_info[0].current_pos[1] - (i + 1) * self.wielkosc_pola)
                        if 0 <= fut_pos[0] <= 7 * self.wielkosc_pola and 0 <= fut_pos[1] <= 7 * self.wielkosc_pola:
                            for klucz, pionek in wlasne.items():
                                if pionek[0].current_pos == fut_pos:
                                    appr = False
                            if appr:
                                for klucz, pionek in cudze.items():
                                    if pionek[0].current_pos == fut_pos:
                                        ruchy.append(fut_pos)
                                        appr = False
                            if appr:
                                ruchy.append(fut_pos)
                    appr = True
                    for i in range(prawa_sciana):
                        fut_pos = (piece_info[0].current_pos[0] + (i + 1) * self.wielkosc_pola,
                                   piece_info[0].current_pos[1] + (i + 1) * self.wielkosc_pola)
                        if 0 <= fut_pos[0] <= 7 * self.wielkosc_pola and 0 <= fut_pos[1] <= 7 * self.wielkosc_pola:
                            for klucz, pionek in wlasne.items():
                                if pionek[0].current_pos == fut_pos:
                                    appr = False
                            if appr:
                                for klucz, pionek in cudze.items():
                                    if pionek[0].current_pos == fut_pos:
                                        ruchy.append(fut_pos)
                                        appr = False
                            if appr:
                                ruchy.append(fut_pos)
                    appr = True
                    for i in range(lewa_sciana):
                        fut_pos = (piece_info[0].current_pos[0] - (i + 1) * self.wielkosc_pola,
                                   piece_info[0].current_pos[1] - (i + 1) * self.wielkosc_pola)
                        if 0 <= fut_pos[0] <= 7 * self.wielkosc_pola and 0 <= fut_pos[1] <= 7 * self.wielkosc_pola:
                            for klucz, pionek in wlasne.items():
                                if pionek[0].current_pos == fut_pos:
                                    appr = False
                            if appr:
                                for klucz, pionek in cudze.items():
                                    if pionek[0].current_pos == fut_pos:
                                        ruchy.append(fut_pos)
                                        appr = False
                            if appr:
                                ruchy.append(fut_pos)
                    appr = True
                    for i in range(lewa_sciana):
                        fut_pos = (piece_info[0].current_pos[0] - (i + 1) * self.wielkosc_pola,
                                   piece_info[0].current_pos[1] + (i + 1) * self.wielkosc_pola)
                        if 0 <= fut_pos[0] <= 7 * self.wielkosc_pola and 0 <= fut_pos[1] <= 7 * self.wielkosc_pola:
                            for klucz, pionek in wlasne.items():
                                if pionek[0].current_pos == fut_pos:
                                    appr = False
                            if appr:
                                for klucz, pionek in cudze.items():
                                    if pionek[0].current_pos == fut_pos:
                                        ruchy.append(fut_pos)
                                        appr = False
                            if appr:
                                ruchy.append(fut_pos)
                    appr = True
                    liczba_ruchow = int((7 * self.wielkosc_pola - piece_info[0].current_pos[1]) / self.wielkosc_pola)
                    for i in range(liczba_ruchow):
                        fut_pos = (piece_info[0].current_pos[0], piece_info[0].current_pos[1] + (i + 1) * self.wielkosc_pola)
                        for klucz, pionek in wlasne.items():
                            if pionek[0].current_pos == fut_pos:
                                appr = False
                        if appr:
                            for klucz, pionek in cudze.items():
                                if pionek[0].current_pos == fut_pos:
                                    ruchy.append(fut_pos)
                                    appr = False
                        if appr:
                            ruchy.append(fut_pos)
                    appr = True
                    liczba_ruchow = int(piece_info[0].current_pos[1] / self.wielkosc_pola)
                    for i in range(liczba_ruchow):
                        fut_pos = (piece_info[0].current_pos[0], piece_info[0].current_pos[1] - (i + 1) * self.wielkosc_pola)
                        for klucz, pionek in wlasne.items():
                            if pionek[0].current_pos == fut_pos:
                                appr = False
                        if appr:
                            for klucz, pionek in cudze.items():
                                if pionek[0].current_pos == fut_pos:
                                    ruchy.append(fut_pos)
                                    appr = False
                        if appr:
                            ruchy.append(fut_pos)
                    appr = True
                    liczba_ruchow = int((7 * self.wielkosc_pola - piece_info[0].current_pos[0]) / self.wielkosc_pola)
                    for i in range(liczba_ruchow):
                        fut_pos = (piece_info[0].current_pos[0] + (i + 1) * self.wielkosc_pola, piece_info[0].current_pos[1])
                        for klucz, pionek in wlasne.items():
                            if pionek[0].current_pos == fut_pos:
                                appr = False
                        if appr:
                            for klucz, pionek in cudze.items():
                                if pionek[0].current_pos == fut_pos:
                                    ruchy.append(fut_pos)
                                    appr = False
                        if appr:
                            ruchy.append(fut_pos)
                    appr = True
                    liczba_ruchow = int(piece_info[0].current_pos[0] / self.wielkosc_pola)
                    for i in range(liczba_ruchow):
                        fut_pos = (piece_info[0].current_pos[0] - (i + 1) * self.wielkosc_pola, piece_info[0].current_pos[1])
                        for klucz, pionek in wlasne.items():
                            if pionek[0].current_pos == fut_pos:
                                appr = False
                        if appr:
                            for klucz, pionek in cudze.items():
                                if pionek[0].current_pos == fut_pos:
                                    ruchy.append(fut_pos)
                                    appr = False
                        if appr:
                            ruchy.append(fut_pos)
                piece_info[2] = ruchy

    def pawn_moves(self, piece):
        ruchy = []
        bicie = []
        appr = True
        wlasne = None
        cudze = None
        kierunek = None
        pion_do_bicia = None
        if piece.druzyna == "biale":
            wlasne = self.biale
            cudze = self.czarne
            kierunek = -1
        elif piece.druzyna == "czarne":
            wlasne = self.czarne
            cudze = self.biale
            kierunek = 1
        fut_pos = (piece.current_pos[0], piece.current_pos[1] + kierunek * self.wielkosc_pola)
        if fut_pos[1] <= 7 * self.wielkosc_pola:
            for klucz, pionek in wlasne.items():
                if pionek[0].current_pos == fut_pos:
                    appr = False
            for klucz, pionek in cudze.items():
                if pionek[0].current_pos == fut_pos:
                    appr = False
            if appr:
                ruchy.append(fut_pos)
                fut_pos = (piece.current_pos[0], piece.current_pos[1] + kierunek * 2 * self.wielkosc_pola)
                appr = True
                if fut_pos[1] <= 7 * self.wielkosc_pola and not piece.has_moved:
                    for klucz, pionek in wlasne.items():
                        if pionek[0].current_pos == fut_pos:
                            appr = False
                    for klucz, pionek in cudze.items():
                        if pionek[0].current_pos == fut_pos:
                            appr = False
                    if appr:
                        ruchy.append(fut_pos)
        appr = False
        fut_pos = (piece.current_pos[0] - self.wielkosc_pola,
                   piece.current_pos[1] + kierunek * self.wielkosc_pola)
        if fut_pos[1] <= 7 * self.wielkosc_pola and 0 <= fut_pos[0] <= 7 * self.wielkosc_pola:
            for klucz, pionek in cudze.items():
                if pionek[0].current_pos == fut_pos:
                    pion_do_bicia = piece.do_bicia = pionek
                    appr = True
            if appr:
                bicie.append([fut_pos, pion_do_bicia])
        appr = False
        fut_pos = (piece.current_pos[0] + self.wielkosc_pola,
                   piece.current_pos[1] + kierunek * self.wielkosc_pola)
        if fut_pos[1] <= 7 * self.wielkosc_pola and 0 <= fut_pos[0] <= 7 * self.wielkosc_pola:
            for klucz, pionek in cudze.items():
                if pionek[0].current_pos == fut_pos:
                    pion_do_bicia = piece.do_bicia = pionek
                    appr = True
            if appr:
                bicie.append([fut_pos, pion_do_bicia])
        return ruchy, bicie

    def losowe_ruchy(self):
        self.mozliwe_ruchy()
        mozliwe_bierki = {typ: bierka for typ, bierka in list(self.czarne.items()) if len(bierka[2]) != 0}
        bierka = random.choice(list(mozliwe_bierki.keys()))
        ruch = random.choice(self.czarne[bierka][2])
        return bierka, ruch

