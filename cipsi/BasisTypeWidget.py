from PyQt4.QtGui import QGroupBox, QSizePolicy, QRadioButton, QHBoxLayout


class BasisTypeWidget(QGroupBox):

    def __init__(self, parent=None):
        super(QGroupBox, self).__init__(parent)
        self.initUI()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def initUI(self):
        self.setTitle("Orbital type")

        radio1 = QRadioButton("&Gaussian")
        radio1.setObjectName("gaussian")
        radio2 = QRadioButton("&Slater")
        radio2.setObjectName("slater")

        vbox = QHBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)
        vbox.addStretch(1)
        self.setLayout(vbox)

    def setGausian(self):
        self.findChild(QRadioButton, "gaussian").setChecked(True)

    def setSlater(self):
        self.findChild(QRadioButton, "slater").setChecked(True)
