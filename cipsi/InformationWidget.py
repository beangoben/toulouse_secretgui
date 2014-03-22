from PyQt4.QtGui import QGroupBox, QSizePolicy, QGridLayout, QLabel, QLineEdit


class InformationWidget(QGroupBox):

    def __init__(self, parent=None):
        super(QGroupBox, self).__init__(parent)
        self.initUI()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def initUI(self):
        self.setTitle('Information')

        grid = QGridLayout()

        label = QLabel("Name : ")
        linedit = QLineEdit()
        linedit.setObjectName("name")

        grid.addWidget(label, 0, 0)
        grid.addWidget(linedit, 0, 1)

        label = QLabel("Nb of elec : ")
        label2 = QLabel("Not yet define")
        label2.setObjectName('nb_e')

        grid.addWidget(label, 1, 0)
        grid.addWidget(label2, 1, 1)

        self.setLayout(grid)

    def setName(self, name):
        self.findChild(QLineEdit, 'name').setText(name)

    def getName(self, name):
        self.findChild(QLineEdit, 'name').getText(name)

    def setNbElec(self, name):
        self.findChild(QLabel, 'nb_e').setText(name)

    def getNbElec(self, name):
        self.findChild(QLabel, 'nb_e').getText(name)
