# QT
from PyQt4.QtCore import *
from PyQt4.QtGui import QTableWidget, QTableWidgetItem, QBrush, QColor
# Python <2.7 suport
try:
    from collections import OrderedDict
except:
    from lib.ordered_dictionary import OrderedDict

# COLORS
red = QBrush(QColor(255, 0, 0))
red.setStyle(Qt.SolidPattern)
white = QBrush(QColor(255, 255, 255))
white.setStyle(Qt.SolidPattern)
blue = QBrush(QColor(51, 153, 255))
blue.setStyle(Qt.SolidPattern)

color = {"red": red, "white": white, "blue": blue}
# Tooltips
dic_orbital_space = OrderedDict([('btn_frozen', 'Frozen orbital'),
                               ('btn_active', 'Active orbital'),
    ('btn_inactive', 'Useless orbital')])


class OrbitalTable(QTableWidget):

    status = []

    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        self.setHorizontalHeaderLabels(['Energy', 'Occu', 'Orbital'])
        print self.getActif()

    def setmydata(self, data):
        self.setRowCount(len(data[data.keys()[0]]))

        for n, key in enumerate(data.keys()):
            for m, item in enumerate(data[key]):
                newitem = QTableWidgetItem(item)
                newitem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.setItem(m, n, newitem)

        for m in data['Energy']:
            if m == ('-'):
                self.status.append(None)
            else:
                self.status.append('Inactive')

    def occu_color(self):
        for r in range(0, self.rowCount()):
            val = int(self.item(r, 2).text())
            if val == 0:
                color = QBrush(QColor(217, 214, 219))
                color.setStyle(Qt.SolidPattern)
                self.item(r, 2).setBackground(color)
            elif val == 1:
                color = QBrush(QColor(122, 125, 128))
                color.setStyle(Qt.SolidPattern)
                self.item(r, 2).setBackground(color)
            elif val == 2:
                color = QBrush(QColor(79, 74, 79))
                color.setStyle(Qt.SolidPattern)
                self.item(r, 2).setBackground(color)

    def setActif(self):
        for idx in self.selectedIndexes():
            self.item(idx.row(), 0).setBackground(color['red'])
            self.item(idx.row(), 1).setBackground(color['red'])
            self.status[idx.row()] = 'Actif'
            print self.getActif()

    def getActif(self):
        return [i for i, j in enumerate(self.status) if j == 'Actif']

    def setInactive(self):
        for idx in self.selectedIndexes():
            self.item(idx.row(), 0).setBackground(color['white'])
            self.item(idx.row(), 1).setBackground(color['white'])
            self.status[idx.row()] = 'Inactive'

    def setFrozen(self):
        for idx in self.selectedIndexes():
            self.item(idx.row(), 0).setBackground(color['blue'])
            self.item(idx.row(), 1).setBackground(color['blue'])
            self.status[idx.row()] = 'Frozen'
