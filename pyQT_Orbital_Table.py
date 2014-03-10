#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
 
data = {'Energy':['5.25','4.32','0.25','-0.98','-1.85','-2.88'],\
        'Occu':['0','0','0','1','2','2'],\
      'Orbital':['5s','4s','1d','3s','2s','1s']}

des_di={'btn_frozen' : 'Frozen orbital'}
 
class MyTable(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setmydata()
        self.occu_color()
 
    def setmydata(self):
 
        horHeaders = []
        for n, key in enumerate(self.data.keys()):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                newitem.setTextAlignment( Qt.AlignHCenter | Qt.AlignVCenter)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)

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

    def color_row(self,color):
          for idx in self.selectedIndexes():
            	self.item(idx.row(),0).setBackground(color)
            	self.item(idx.row(),1).setBackground(color)

class OrbitalClass(QWidget):
    
  def __init__(self):
        super(OrbitalClass, self).__init__()
        
        self.initUI()
        
  def initUI(self):
        table = MyTable(data, 6, 3,self)
        table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        red=QBrush(QColor(255, 0, 0))
        red.setStyle(Qt.SolidPattern)

        white=QBrush(QColor(255, 255, 255))
        white.setStyle(Qt.SolidPattern)

        blue=QBrush(QColor(51, 153 , 255))
        blue.setStyle(Qt.SolidPattern)

        btn_actif = QPushButton('Actif', self)
        btn_actif.setStyleSheet("background-color: red")
        btn_actif.clicked.connect(lambda: table.color_row(red))

        btn_frozen = QPushButton('Frozen', self)
        btn_frozen.setStyleSheet("background-color: rgb(51,153,255)")
        btn_frozen.clicked.connect(lambda: table.color_row(blue))
        btn_frozen.setStatusTip(des_di["btn_frozen"])

        btn_inactif = QPushButton('Inactif', self)
        btn_inactif.setStyleSheet("background-color: white")
        btn_inactif.clicked.connect(lambda: table.color_row(white))

        vbox = QVBoxLayout()
        vbox.addWidget(table)
        vbox.addWidget(btn_actif)
        vbox.addWidget(btn_frozen)
        vbox.addWidget(btn_inactif)

        self.setLayout(vbox)
       # self.show()    

class total(QWidget):
  def __init__(self, parent=None):
        super(total, self).__init__(parent)
        self.initUI()	

  def initUI(self):
        grid = QGridLayout()

        sub_vbox=QVBoxLayout()

        sub_vbox.addWidget(self.createBasisTypeGroup())
        sub_vbox.addWidget(self.createTargetSpaceGroup())
        sub_vbox.addWidget(self.createStopingCriteriumGroup())

        sub_vbox.addWidget(QWidget())
         
        grid.addLayout(sub_vbox,0,0,0,2)
        grid.addWidget(self.createOrbitalClassGroup(), 0, 2)

        self.setLayout(grid)

        self.setWindowTitle("Group Box")
        self.resize(480, 320)

  def createOrbitalClassGroup(self):
        groupBox = QGroupBox("Orbital class")

        vbox = QVBoxLayout()
        vbox.addWidget(OrbitalClass())

        groupBox.setLayout(vbox)

        return groupBox

  def createTargetSpaceGroup(self):
        groupBox = QGroupBox("Target Space")

        radio1 = QRadioButton("&Full CI")
        radio2 = QRadioButton("CISD")
        radio3 = QRadioButton("Super CI (Hartree Fock)")

        targetSpaceList=["HF (super CI)",
                         "CISD",
                         "Full CI"]

        comboBox=QComboBox()
        comboBox.addItems(targetSpaceList)

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)
        vbox.addWidget(radio3)
        #vbox.addWidget(comboBox)

        vbox.addStretch(1)

        groupBox.setLayout(vbox)
        groupBox.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Fixed)
        return groupBox
  def createBasisTypeGroup(self):
        groupBox = QGroupBox("Orbital type")
        radio1 = QRadioButton("&Gaussian")
        radio2 = QRadioButton("&Slater")

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        groupBox.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Fixed)
        return groupBox
  def CoolBoxLayout(self,name):
        hbox = QHBoxLayout()
        chBox=QCheckBox(name,self)
        hbox.addWidget(chBox)
        edit= QLineEdit(self)
        hbox.addWidget(edit)
   
        return hbox

  def createStopingCriteriumGroup(self):
       groupBox = QGroupBox("Stoping criterum")
        

       vbox = QVBoxLayout()

       dump=self.CoolBoxLayout('PT1')
       vbox.addLayout(dump)
   
       dump=self.CoolBoxLayout('PT2')
       vbox.addLayout(dump)

       dump=self.CoolBoxLayout('Nb determinant')
       vbox.addLayout(dump)

       vbox.addStretch(1)
       groupBox.setLayout(vbox)
       groupBox.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Fixed)
       return groupBox

class MainWindow(QMainWindow):

    def printAct(self):
        self.statusBar.showMessage('clike')

    def __init__(self):
        super(MainWindow, self).__init__()
     


        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('Welcom to the GUI')


        widget = total()
        self.setCentralWidget(widget)

        self.setWindowTitle("Menus")
        self.setMinimumSize(160,160)
        self.resize(550,320)


def main(args):
    app = QApplication(args)
    app.setStyle(QStyleFactory.create("plastique"))
  

    #ex=total()
    ex=MainWindow()
    ex.show()

    sys.exit(app.exec_())
 
if __name__=="__main__":
    main(sys.argv)