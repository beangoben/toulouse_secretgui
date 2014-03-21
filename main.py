#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import  QGroupBox, QMainWindow, QApplication, QStyleFactory, QStatusBar, QAction, QGridLayout, QVBoxLayout,  QSizePolicy, QHBoxLayout, QBoxLayout, QHeaderView, QBrush, QColor, QFileDialog
from PyQt4.QtGui import  QWidget, QTableWidget, QTabWidget, QLabel, QLineEdit, QRadioButton, QCheckBox, QPushButton, QTableWidgetItem
from PyQt4.QtGui import  QSpinBox, QDoubleSpinBox,QPalette

from parsers.slater_parser import slater_wraper

#Python <2.7 suport
try :
    from collections import OrderedDict
except :
    from lib.ordered_dictionary import OrderedDict

dic_orbital_space=OrderedDict([('btn_frozen','Frozen orbital'),
                              ('btn_active','Active orbital'),
                              ('btn_inactive','Ussless orbital')
                              ])


dic_target_space=OrderedDict([('Hartree Fock','For the weak'),
                              ('CISD',"When you can't do beter"),
                              ('FullCI','Is the best')
                              ])

dic_stoping_criterum=OrderedDict([('PT1 :',"Maybe Perturbated energy order 1"),
                                  ('PT2 :','Perturbated energy order 2'),
                                  ('Nb Det :',"The number of determinant. Surprising no ?")
                                 ])

red   =QBrush(QColor(255, 0, 0))       ; red.setStyle(Qt.SolidPattern)
white =QBrush(QColor(255, 255 , 255))  ; white.setStyle(Qt.SolidPattern)
blue  =QBrush(QColor(51, 153 , 255))   ; blue.setStyle(Qt.SolidPattern)

color={"red":red,"white":white,"blue":blue}

class orbitalTable(QTableWidget):

    status=[]

    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        self.setHorizontalHeaderLabels(['Energy','Occu', 'Orbital'])
        print self.getActif()

    def setmydata(self,data):
        self.setRowCount(len(data[data.keys()[0]]))

        for n, key in enumerate(data.keys()):
            for m, item in enumerate(data[key]):
                newitem = QTableWidgetItem(item)
                newitem.setTextAlignment( Qt.AlignHCenter | Qt.AlignVCenter)
                self.setItem(m, n, newitem)

        for m in data['Energy']:
                if m==('-'):
                   self.status.append(None)
                else:
                   self.status.append('Inactive')

    def occu_color(self):
        for r in range(0,self.rowCount()):
            val=int(self.item(r,2).text())
            if val==0:
                color=QBrush(QColor(217, 214, 219))
                color.setStyle(Qt.SolidPattern)
                self.item(r,2).setBackground(color)
            elif val==1:
                color=QBrush(QColor(122, 125, 128))
                color.setStyle(Qt.SolidPattern)
                self.item(r,2).setBackground(color)
            elif val==2:
                color=QBrush(QColor(79, 74, 79))
                color.setStyle(Qt.SolidPattern)
                self.item(r,2).setBackground(color)

    def setActif(self):
         for idx in self.selectedIndexes():
            self.item(idx.row(),0).setBackground(color['red'])
            self.item(idx.row(),1).setBackground(color['red'])
            self.status[idx.row()]='Actif'
            print self.getActif()

    def getActif(self):
        return [i for i,j in enumerate(self.status) if j=='Actif']

    def setInactive(self):
        for idx in self.selectedIndexes():
            self.item(idx.row(),0).setBackground(color['white'])
            self.item(idx.row(),1).setBackground(color['white'])
            self.status[idx.row()]='Inactive'

    def setFrozen(self):
        for idx in self.selectedIndexes():
            self.item(idx.row(),0).setBackground(color['blue'])
            self.item(idx.row(),1).setBackground(color['blue'])
            self.status[idx.row()]='Frozen'




class orbitalWidget(QGroupBox):

    def __init__(self):
        super(QGroupBox, self).__init__()

        self.initUI()

    def initUI(self):

        table= orbitalTable(0, 3)
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

        w=QWidget()

        w.setLayout(vbox)

        self.setTitle("Orbital class")

        vbox = QVBoxLayout()
        vbox.addWidget(w)
        self.setLayout(vbox)

class informationWidget(QGroupBox):

    def __init__(self, parent=None):
        super(QGroupBox, self).__init__(parent)
        self.initUI()
        self.setSizePolicy(QSizePolicy.Expanding , QSizePolicy.Fixed)

    def initUI(self):
        self.setTitle('Information')

        grid = QGridLayout()

        label= QLabel("Name : ")
        linedit = QLineEdit() ; linedit.setObjectName("name")

        grid.addWidget(label,0,0)
        grid.addWidget(linedit,0,1)

        label= QLabel("Nb of elec : ")
        label2=QLabel("Not yet define") ; label2.setObjectName('nb_e')

        grid.addWidget(label,1,0)
        grid.addWidget(label2,1,1)

        self.setLayout(grid)

    def setName(self,name):
        self.findChild(QLineEdit,'name').setText(name)

    def getName(self,name):
        self.findChild(QLineEdit,'name').getText(name)

    def setNbElec(self,name):
        self.findChild(QLabel,'nb_e').setText(name)

    def getNbElec(self,name):
        self.findChild(QLabel,'nb_e').getText(name)

class  basisTypeWidget(QGroupBox):

    def __init__(self, parent=None):
        super(QGroupBox, self).__init__(parent)
        self.initUI()
        self.setSizePolicy(QSizePolicy.Expanding , QSizePolicy.Fixed)

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

class  targetSpaceWidget(QGroupBox):

    def __init__(self, parent=None):
        super(QGroupBox, self).__init__(parent)
        self.initUI()
        self.setSizePolicy(QSizePolicy.Expanding , QSizePolicy.Fixed)

    def initUI(self):
        self.setTitle("Target Space")

        vbox = QVBoxLayout()
        vbox=QBoxLayout(QBoxLayout.LeftToRight)

        for name,description in dic_target_space.items():
            qb=QRadioButton(name)
            qb.setStatusTip(description)
            vbox.addWidget(qb)

        vbox.addStretch(1)
        self.setLayout(vbox)


class mySpinBoxWidget(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        vbox=QHBoxLayout()

        edit=QDoubleSpinBox(self)
        edit.setLocale(QLocale(QLocale.English))
        edit.setDecimals(2)
        vbox.addWidget(edit)

        vbox.addWidget(QLabel("10^"))

        expo=QSpinBox(self)
        expo.setMinimum(-8)
        expo.setMaximum(8)
        vbox.addWidget(expo)

        self.setLayout(vbox)

    def getValue(self):
        digit=self.findChild(QDoubleSpinBox).value()
        power=self.findChild(QSpinBox).value()

        return digit*pow(10,power)

class  StopingCriteriumWidget(QGroupBox):

    def __init__(self, parent=None):
        super(QGroupBox, self).__init__(parent)
        self.initUI()
        self.setSizePolicy(QSizePolicy.Expanding , QSizePolicy.Fixed)

    def initUI(self):

        self.setTitle("Stoping criterum")

        grid = QGridLayout()
        grid.setVerticalSpacing(0)

        for i,(name,description) in enumerate(dic_stoping_criterum.items()):
            chBox=QCheckBox(name,self); chBox.setStatusTip(description)
            grid.addWidget(chBox, i, 0)

            cb=mySpinBoxWidget(self); cb.setObjectName(name)
            grid.addWidget(cb,i,1)


        self.setLayout(grid)

class cipsiWidget(QWidget):
    def __init__(self, parent=None):
        super(cipsiWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        sub_vbox=QVBoxLayout()

        sub_vbox.addWidget(informationWidget())
        sub_vbox.addWidget(basisTypeWidget())
        sub_vbox.addWidget(targetSpaceWidget())
        sub_vbox.addWidget(StopingCriteriumWidget())

        sub_vbox.addWidget(QWidget())

        grid.addLayout(sub_vbox,0,0,0,2)
        grid.addWidget(orbitalWidget(), 0, 2)

        self.setLayout(grid)

        self.setWindowTitle("Group Box")
        self.resize(480, 320)

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('Welcom to the GUI')


        openFile = QAction('Open File', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File (like gamess, Bunge Slater)')
        openFile.triggered.connect(self.showDialogFile)


        openEZFIO = QAction('Open EZFIO', self)
        openEZFIO.setShortcut('Ctrl+E')
        openEZFIO.setStatusTip('Open new EZFIO')
        openEZFIO.triggered.connect(self.showDialogFolderRead)


        saveToEZFIO = QAction('Save to EZFIO', self)
        saveToEZFIO.setShortcut('Ctrl+S')
        saveToEZFIO.setStatusTip('Save on folder EZFIO proof')
        saveToEZFIO.triggered.connect(self.showDialogFolderSave)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(openEZFIO)
        fileMenu.addAction(saveToEZFIO)

        tab_widget = QTabWidget()
        tab1 = cipsiWidget()
        tab2 = QWidget()
        tab_widget.addTab(tab1, "CIPSI")
        tab_widget.addTab(tab2, "QMC")
        self.setCentralWidget(tab_widget)

        self.setWindowTitle("Pig Is a Gui")
        self.setMinimumSize(160,160)
        self.resize(800,500)

    def showDialogFile(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setOption(QFileDialog.ShowDirsOnly, False)
        dialog.setOption(QFileDialog.ReadOnly, True)

        if dialog.exec_():
            for d in dialog.selectedFiles():

                global wrater

                wrater=slater_wraper(d)

                ot=self.findChild(orbitalTable)
                ot.setmydata({'Energy': wrater.get_mo_energy(),
                              'Occu' : wrater.get_mo_occ(),
                              'Orbital' : wrater.get_mo_name()})

                bt=self.findChild(basisTypeWidget)
                bt.setSlater()

                iw=self.findChild(informationWidget)
                iw.setName("He")
                iw.setNbElec("6")

    def showDialogFolderRead(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)

        if dialog.exec_():
            for d in dialog.selectedFiles():
                print d

    def showDialogFolderSave(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)

        for name in dic_stoping_criterum:
            d=self.findChild(mySpinBoxWidget,name)
            print name,d.getValue()

        if dialog.exec_():
            for d in dialog.selectedFiles():
                wrater.write_ezfio(str(d))


def main(args):
    app = QApplication(args)
    app.setStyle(QStyleFactory.create("plastique"))
    ex=MainWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main(sys.argv)
