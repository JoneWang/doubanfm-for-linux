#!/usr/bin/env python2
# coding: UTF-8

import sys

if __name__ == "__main__":
    ''' 
    #start as a normal app
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("Douban FM")
    doubanfm = DoubanFMGUI()
    doubanfm.show()
    sys.exit(app.exec_())
    '''

    # start as a tray bar app
    from gui import SystemTrayApp
    from PyQt4 import QtGui
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("Douban FM")
    app.setQuitOnLastWindowClosed(False)
    w = app.desktop().width()
    h = app.desktop().height()
    widget = QtGui.QWidget()
    doubanfm = SystemTrayApp(widget, w, h)
    doubanfm.show()
    sys.exit(app.exec_())
