from PyQt4.QtGui import QGroupBox, QSizePolicy, QRadioButton
from PyQt4.QtGui import QBoxLayout, QVBoxLayout

# Python <2.7 suport
try:
    from collections import OrderedDict
except:
    from lib.ordered_dictionary import OrderedDict

dic_target_space = OrderedDict([('Hartree Fock', 'For the weak'),
                              ('CISD', "When you can't do beter"),
                              ('FullCI', 'Is the best')])


class TargetSpaceWidget(QGroupBox):

    def __init__(self, parent=None):
        super(QGroupBox, self).__init__(parent)
        self.initUI()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def initUI(self):
        self.setTitle("Target Space")
        vbox = QVBoxLayout()
        vbox = QBoxLayout(QBoxLayout.LeftToRight)
        for name, description in dic_target_space.items():
            qb = QRadioButton(name)
            qb.setStatusTip(description)
            vbox.addWidget(qb)

        vbox.addStretch(1)
        self.setLayout(vbox)
