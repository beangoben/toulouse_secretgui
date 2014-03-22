from PyQt4.QtCore import *
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QWidget, QHBoxLayout, QDoubleSpinBox, QSpinBox


class MySpinBoxWidget(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):

        vbox = QHBoxLayout()
        edit = QDoubleSpinBox(self)
        edit.setLocale(QLocale(QLocale.English))
        edit.setDecimals(2)
        vbox.addWidget(edit)
        vbox.addWidget(QLabel("10^"))
        expo = QSpinBox(self)
        expo.setMinimum(-8)
        expo.setMaximum(8)
        vbox.addWidget(expo)
        self.setLayout(vbox)

    def getValue(self):
        digit = self.findChild(QDoubleSpinBox).value()
        power = self.findChild(QSpinBox).value()

        return digit * pow(10, power)
