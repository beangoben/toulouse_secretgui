#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT
import sys

class myTabWidget(QtGui.QTabWidget):

  @pyqtSlot(int)
  def tabChangedSlot(self,argTabIndex):
    QtGui.QMessageBox.information(self,
                  "Tab Index Changed!",
                  "Current Tab Index: "+QtCore.QString.number(argTabIndex));


def main():
    app      = QtGui.QApplication(sys.argv)
    tabWidget    = myTabWidget()
    tabWidget.addTab(QtGui.QWidget(),"1");
    tabWidget.addTab(QtGui.QWidget(),"2");
    tabWidget.addTab(QtGui.QWidget(),"3");

    #Resize width and height
    tabWidget.resize(300,120)
    tabWidget.setWindowTitle('QTabWidget Changed Example')

    tabWidget.connect(tabWidget,SIGNAL("currentChanged(int)"),tabWidget,SLOT("tabChangedSlot(int)"))


    tabWidget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

