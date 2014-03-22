from PyQt4.QtGui import QGroupBox, QPushButton, QHeaderView, QVBoxLayout
from PyQt4.QtGui import QWidget
from OrbitalTable import *


class OrbitalWidget(QGroupBox):

    def __init__(self):
        super(QGroupBox, self).__init__()

        self.initUI()

    def initUI(self):

        table = OrbitalTable(0, 3)
        table.horizontalHeader().setResizeMode(QHeaderView.Stretch)

        btn_active = QPushButton('Active', self)

        btn_active.setStyleSheet("background-color: red")
        btn_active.clicked.connect(table.setActif)
        btn_active.setStatusTip(dic_orbital_space["btn_active"])

        btn_frozen = QPushButton('Frozen', self)
        btn_frozen.setStyleSheet("background-color: rgb(51,153,255)")
        btn_frozen.clicked.connect(table.setFrozen)
        btn_frozen.setStatusTip(dic_orbital_space["btn_frozen"])

        btn_inactive = QPushButton('Inactive', self)
        btn_inactive.setStyleSheet("background-color: white")
        btn_inactive.clicked.connect(table.setInactive)
        btn_inactive.setStatusTip(dic_orbital_space["btn_inactive"])

        vbox = QVBoxLayout()
        vbox.addWidget(table)
        vbox.addWidget(btn_active)
        vbox.addWidget(btn_frozen)
        vbox.addWidget(btn_inactive)

        w = QWidget()

        w.setLayout(vbox)

        self.setTitle("Orbital class")

        vbox = QVBoxLayout()
        vbox.addWidget(w)
        self.setLayout(vbox)
