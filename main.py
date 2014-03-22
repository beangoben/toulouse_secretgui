#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import QMainWindow, QApplication, QStyleFactory, QStatusBar
from PyQt4.QtGui import QWidget, QTabWidget, QAction, QFileDialog, QMenu, QIcon

from parsers.slater_parser import slater_wraper
from cipsi.CipsiWidget import *


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

        inputCipsi = QAction('CIPSI', self)
        inputCipsi.setStatusTip('create/edit CIPSI input')
        inputCipsi.triggered.connect(self.creatCipsiInputTab)

        inputQMC = QAction('QMC', self)
        inputQMC.setStatusTip('create/edit QMC input')
        inputQMC.triggered.connect(self.creatQMCInputTab)

        input_menu = QMenu("Input", self)
        input_menu.addAction(inputQMC)
        input_menu.addAction(inputCipsi)

        outputCipsi = QAction('CIPSI', self)
        outputCipsi.setStatusTip('create/edit CIPSI output')
        outputCipsi.triggered.connect(self.emptySlot)

        outputQMC = QAction('QMC', self)
        outputQMC.setStatusTip('create/edit QMC output')
        outputQMC.triggered.connect(self.emptySlot)

        output_menu = QMenu("Output", self)
        output_menu.addAction(outputQMC)
        output_menu.addAction(outputCipsi)

        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QApplication.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(openEZFIO)
        fileMenu.addAction(saveToEZFIO)
        fileMenu.addMenu(input_menu)
        fileMenu.addMenu(output_menu)
        fileMenu.addAction(exitAction)

        helpMenu = menubar.addMenu('&Help')


        tab_widget = QTabWidget()
        tab_widget.setTabsClosable(True)
        tab_widget.tabCloseRequested.connect(tab_widget.removeTab)
        self.setCentralWidget(tab_widget)
        self.tab_widget=tab_widget

        self.setWindowTitle("Pig Is a Gui")
        self.setMinimumSize(160, 160)
        self.resize(800, 500)

    def showDialogFile(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setOption(QFileDialog.ShowDirsOnly, False)
        dialog.setOption(QFileDialog.ReadOnly, True)

        if dialog.exec_():
            for d in dialog.selectedFiles():

                global wrater

                wrater = slater_wraper(d)

                ot = self.findChild(orbitalTable)
                ot.setmydata({'Energy': wrater.get_mo_energy(),
                              'Occu': wrater.get_mo_occ(),
                              'Orbital': wrater.get_mo_name()})

                bt = self.findChild(basisTypeWidget)
                bt.setSlater()

                iw = self.findChild(informationWidget)
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
            d = self.findChild(mySpinBoxWidget, name)
            print name, d.getValue()

        if dialog.exec_():
            for d in dialog.selectedFiles():
                wrater.write_ezfio(str(d))

    def creatCipsiInputTab(self):
        tab = CipsiWidget()
        self.tab_widget.addTab(tab, "CIPSI input")

    def creatQMCInputTab(self):
        tab = QWidget()
        self.tab_widget.addTab(tab, "QMC input")

    def emptySlot(self):
        return


def main(args):
    app = QApplication(args)
    app.setStyle(QStyleFactory.create("plastique"))
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv)
