import traceback

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import colors
from map import Map

MAP_SIZE = 10


class GameUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.mainLayout = QVBoxLayout()

        hLayout = QHBoxLayout()

        resetButton = QToolButton()
        resetButton.setText("Reset")
        resetButton.clicked.connect(self.resetMap)

        self.result = QLabel()
        self.result.setText("")

        hLayout.addWidget(resetButton)
        hLayout.addStretch(1)
        hLayout.addWidget(self.result)

        self.mainLayout.addLayout(hLayout)

        mapLayout = QGridLayout()

        self.map_ = Map().makeMap(MAP_SIZE)
        self.known_map = [[False for x in range(MAP_SIZE)] for y in range(MAP_SIZE)]
        self.btns = [[None for y in range(MAP_SIZE)] for x in range(MAP_SIZE)]

        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                btn = MyButton(str(self.map_[i][j]), self.buttonClicked)
                mapLayout.addWidget(btn, i, j)
                self.btns[i][j] = btn

        self.mainLayout.addLayout(mapLayout)

        self.setLayout(self.mainLayout)

        self.setWindowTitle("지뢰 찾기")

    def resetMap(self):
        try:
            self.map_ = Map().makeMap(MAP_SIZE)
            self.known_map = [[False for x in range(MAP_SIZE)] for y in range(MAP_SIZE)]
            self.result.setText("0")

            for i in range(MAP_SIZE):
                for j in range(MAP_SIZE):
                    text = str(self.map_[i][j])
                    btn: QToolButton = self.btns[i][j]
                    btn.setText("")
                    btn.setStyleSheet(colors.unknown)
                    btn.setEnabled(True)
                    btn.setToolButtonStyle(Qt.ToolButtonTextOnly)
        except:
            print(traceback.format_exc())

    def endGame(self, text):
        for x in range(MAP_SIZE):
            for y in range(MAP_SIZE):
                if self.map_[x][y] == 5:
                    self.btns[x][y].setIcon(QIcon('bomb.png'))
                    self.btns[x][y].setToolButtonStyle(Qt.ToolButtonIconOnly)
                self.btns[x][y].setDisabled(True)
                self.result.setText(text)

    def isGameEnd(self):
        for x in range(MAP_SIZE):
            for y in range(MAP_SIZE):
                if self.map_[x][y] != 5 and not self.known_map[x][y]:
                    return False
        return True

    def buttonClicked(self):
        try:
            btn: QToolButton = self.sender()
            idx = self.findIndex(btn)
            text = str(self.map_[idx[1]][idx[0]])
            self.known_map[idx[1]][idx[0]] = True
            if text == "0":
                self.findSafeZone(idx[0], idx[1])
                btn.setStyleSheet(colors.known)
            elif text == "1":
                btn.setStyleSheet(colors.risky + "; " + colors.known)
                btn.setText(text)
            elif text == "2":
                btn.setStyleSheet(colors.dangerous + "; " + colors.known)
                btn.setText(text)
            elif text == "3":
                btn.setStyleSheet(colors.hazardous + "; " + colors.known)
                btn.setText(text)
            elif text == "4":
                btn.setStyleSheet(colors.atStake + "; " + colors.known)
                btn.setText(text)
            elif text == "5":
                btn.setIcon(QIcon('bomb.png'))
                btn.setToolButtonStyle(Qt.ToolButtonIconOnly)
                print("boom")
                self.endGame("Fall...")
                btn.setStyleSheet("background-color: red")
            else:
                btn.setText(text)
            btn.setDisabled(True)
            if self.isGameEnd():
                self.endGame("Win!")
        except Exception:
            print(traceback.format_exc())

    def findSafeZone(self, x, y):
        around = [
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1)
        ]
        for dx, dy in around:
            if (y + dy) < 0 or (y + dy) >= MAP_SIZE or (x + dx) < 0 or (x + dx) >= MAP_SIZE:
                continue
            if self.known_map[y + dy][x + dx]:
                continue
            if self.map_[y + dy][x + dx] == 0:
                self.known_map[y + dy][x + dx] = True
                self.btns[y + dy][x + dx].click()

    def findIndex(self, btn):
        for x in range(MAP_SIZE):
            for y in range(MAP_SIZE):
                if btn == self.btns[y][x]:
                    return [x, y]


class MyButton(QToolButton):
    def __init__(self, text, callback):
        super().__init__()
        self.setFixedSize(QSize(40, 40))
        self.setSizePolicy(QSizePolicy.Expanding,
                           QSizePolicy.Preferred)
        # else:
        #    self.setText(text)
        self.setStyleSheet(colors.unknown)
        self.clicked.connect(callback)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    calc = GameUI()
    calc.show()
    sys.exit(app.exec_())
