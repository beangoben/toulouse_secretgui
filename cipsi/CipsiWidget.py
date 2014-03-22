from OrbitalWidget import *
from StopingCriteriumWidget import *
from BasisTypeWidget import *
from TargetSpaceWidget import *
from InformationWidget import *

from PyQt4.QtGui import QWidget, QGridLayout, QVBoxLayout


class CipsiWidget(QWidget):

    def __init__(self, parent=None):
        super(CipsiWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        sub_vbox = QVBoxLayout()
        sub_vbox.addWidget(InformationWidget())
        sub_vbox.addWidget(BasisTypeWidget())
        sub_vbox.addWidget(TargetSpaceWidget())
        sub_vbox.addWidget(StopingCriteriumWidget())
        sub_vbox.addWidget(QWidget())
        grid.addLayout(sub_vbox, 0, 0, 0, 2)
        grid.addWidget(OrbitalWidget(), 0, 2)
        self.setLayout(grid)
        self.setWindowTitle("Group Box")
        self.resize(480, 320)
