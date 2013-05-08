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
    from gui import SystemTrayIcon
    from PyQt4 import QtGui
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("Douban FM")
    app.setQuitOnLastWindowClosed(False)
    w = QtGui.QWidget()
    trayIcon = SystemTrayIcon(w)
    trayIcon.show()
    sys.exit(app.exec_())
