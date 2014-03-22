from PyQt4.QtGui import QGroupBox, QSizePolicy, QGridLayout, QCheckBox
from MySpinBoxWidget import *
# Python <2.7 suport
try:
    from collections import OrderedDict
except:
    from lib.ordered_dictionary import OrderedDict

dic_stoping_criterum = OrderedDict(
    [('PT1 :', "Maybe Perturbated energy order 1"),
     ('PT2 :', 'Perturbated energy order 2'),
     ('Nb Det :', "The number of determinant. Surprising no ?")
     ])


class StopingCriteriumWidget(QGroupBox):

    def __init__(self, parent=None):
        super(QGroupBox, self).__init__(parent)
        self.initUI()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def initUI(self):

        self.setTitle("Stoping criterum")

        grid = QGridLayout()
        grid.setVerticalSpacing(0)

        for i, (name, description) in enumerate(dic_stoping_criterum.items()):
            chBox = QCheckBox(name, self)
            chBox.setStatusTip(description)
            grid.addWidget(chBox, i, 0)

            cb = MySpinBoxWidget(self)
            cb.setObjectName(name)
            grid.addWidget(cb, i, 1)

        self.setLayout(grid)
