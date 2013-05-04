# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/player.ui'
#
# Created: Sat May  4 16:10:11 2013
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(400, 400)
        MainWindow.setMinimumSize(QtCore.QSize(400, 200))
        MainWindow.setMaximumSize(QtCore.QSize(400, 400))
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(_fromUtf8("background-color: rgba(255,255,255);"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 408, 202))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButtonCover = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButtonCover.setMinimumSize(QtCore.QSize(200, 200))
        self.pushButtonCover.setMaximumSize(QtCore.QSize(200, 200))
        self.pushButtonCover.setStyleSheet(_fromUtf8("border: none;\n"
"outline: none;"))
        self.pushButtonCover.setText(_fromUtf8(""))
        self.pushButtonCover.setAutoDefault(True)
        self.pushButtonCover.setFlat(True)
        self.pushButtonCover.setObjectName(_fromUtf8("pushButtonCover"))
        self.horizontalLayout_2.addWidget(self.pushButtonCover)
        self.widget = QtGui.QWidget(self.horizontalLayoutWidget_2)
        self.widget.setMinimumSize(QtCore.QSize(200, 200))
        self.widget.setMaximumSize(QtCore.QSize(200, 200))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.labelArtist = QtGui.QLabel(self.widget)
        self.labelArtist.setGeometry(QtCore.QRect(10, 30, 181, 31))
        self.labelArtist.setStyleSheet(_fromUtf8("color: \'#333\';\n"
"font: 22px/1.2 \"Helvetica Neue\",Helvetica,Arial,sans-serif"))
        self.labelArtist.setObjectName(_fromUtf8("labelArtist"))
        self.labelAlbum = QtGui.QLabel(self.widget)
        self.labelAlbum.setGeometry(QtCore.QRect(10, 60, 181, 16))
        self.labelAlbum.setStyleSheet(_fromUtf8("color: \'#333\';\n"
"font: 12px/1.2 \"Helvetica Neue\",Helvetica,Arial,sans-serif"))
        self.labelAlbum.setObjectName(_fromUtf8("labelAlbum"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 160, 152, 32))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(30)
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonHeart = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButtonHeart.setMinimumSize(QtCore.QSize(28, 28))
        self.pushButtonHeart.setMaximumSize(QtCore.QSize(28, 28))
        self.pushButtonHeart.setStyleSheet(_fromUtf8("border-image: url(:/player/heart.png);\n"
"border: none;\n"
"outline: none;"))
        self.pushButtonHeart.setText(_fromUtf8(""))
        self.pushButtonHeart.setAutoDefault(True)
        self.pushButtonHeart.setFlat(True)
        self.pushButtonHeart.setObjectName(_fromUtf8("pushButtonHeart"))
        self.horizontalLayout.addWidget(self.pushButtonHeart)
        self.pushButtonTrash = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButtonTrash.setMinimumSize(QtCore.QSize(28, 28))
        self.pushButtonTrash.setMaximumSize(QtCore.QSize(28, 28))
        self.pushButtonTrash.setStyleSheet(_fromUtf8("border-image: url(:/player/trash.png);\n"
"border: none;\n"
"outline: none;"))
        self.pushButtonTrash.setText(_fromUtf8(""))
        self.pushButtonTrash.setAutoDefault(True)
        self.pushButtonTrash.setFlat(True)
        self.pushButtonTrash.setObjectName(_fromUtf8("pushButtonTrash"))
        self.horizontalLayout.addWidget(self.pushButtonTrash)
        self.pushButtonSkip = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButtonSkip.setMinimumSize(QtCore.QSize(28, 28))
        self.pushButtonSkip.setMaximumSize(QtCore.QSize(28, 28))
        self.pushButtonSkip.setStyleSheet(_fromUtf8("border-image: url(:/player/skip.png);\n"
"border: none;\n"
"outline: none;"))
        self.pushButtonSkip.setText(_fromUtf8(""))
        self.pushButtonSkip.setAutoDefault(True)
        self.pushButtonSkip.setFlat(True)
        self.pushButtonSkip.setObjectName(_fromUtf8("pushButtonSkip"))
        self.horizontalLayout.addWidget(self.pushButtonSkip)
        self.pushButtonToggle = QtGui.QPushButton(self.widget)
        self.pushButtonToggle.setGeometry(QtCore.QRect(130, 0, 28, 28))
        self.pushButtonToggle.setMinimumSize(QtCore.QSize(28, 28))
        self.pushButtonToggle.setMaximumSize(QtCore.QSize(28, 28))
        self.pushButtonToggle.setStyleSheet(_fromUtf8("background: url(:/player/pause.png) no-repeat center;\n"
"border: none;\n"
"outline: none;\n"
"background-color: \'#9dd6c5\';\n"
"border-radius: 1px;\n"
""))
        self.pushButtonToggle.setText(_fromUtf8(""))
        self.pushButtonToggle.setAutoDefault(True)
        self.pushButtonToggle.setObjectName(_fromUtf8("pushButtonToggle"))
        self.timeLabel = QtGui.QLabel(self.widget)
        self.timeLabel.setGeometry(QtCore.QRect(130, 110, 45, 27))
        self.timeLabel.setObjectName(_fromUtf8("timeLabel"))
        self.seekSlider = phonon.Phonon.SeekSlider(self.widget)
        self.seekSlider.setGeometry(QtCore.QRect(10, 96, 171, 21))
        self.seekSlider.setMinimumSize(QtCore.QSize(150, 10))
        self.seekSlider.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.seekSlider.setStyleSheet(_fromUtf8("QSlider::groove:horizontal {\n"
"     border: none;\n"
"     height: 2px;\n"
"     background: \'#EEE\';\n"
" }\n"
"\n"
" QSlider::handle:horizontal {\n"
"     background: \'#9dd6c5\';\n"
"     border: none;\n"
"     width: 18px;\n"
"     margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */\n"
"     border-radius: 1px;\n"
" }\n"
"\n"
"QSlider::add-page:horizontal {\n"
"     background: \'#EEE\';\n"
"     border: none;\n"
" }\n"
"\n"
" QSlider::sub-page:horizontal {\n"
"     background: \'#9dd6c5\';\n"
"     border: none;\n"
" }"))
        self.seekSlider.setObjectName(_fromUtf8("seekSlider"))
        self.volumeSlider = phonon.Phonon.VolumeSlider(self.widget)
        self.volumeSlider.setGeometry(QtCore.QRect(100, 130, 81, 20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.volumeSlider.sizePolicy().hasHeightForWidth())
        self.volumeSlider.setSizePolicy(sizePolicy)
        self.volumeSlider.setMinimumSize(QtCore.QSize(50, 0))
        self.volumeSlider.setStyleSheet(_fromUtf8("QSlider::groove:horizontal {\n"
"    border: none;\n"
"    height: 2px;\n"
"    background: \'#EEE\';\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"    background: \'#9dd6c5\';\n"
"    height: 2px;\n"
"    border: none;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"    background: \'#EEE\';\n"
"    height: 2px;\n"
"    border: none;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: \'#9dd6c5\';\n"
"    border: none;\n"
"    width: 6px;\n"
"    border-radius: 1px;\n"
"}"))
        self.volumeSlider.setObjectName(_fromUtf8("volumeSlider"))
        self.labelTitle = QtGui.QLabel(self.widget)
        self.labelTitle.setGeometry(QtCore.QRect(10, 80, 181, 16))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.labelTitle.setFont(font)
        self.labelTitle.setWhatsThis(_fromUtf8(""))
        self.labelTitle.setStyleSheet(_fromUtf8("color: \'#9dd6c5\';\n"
"font: 16px/1.2 \"Helvetica Neue\",Helvetica,Arial,sans-serif"))
        self.labelTitle.setObjectName(_fromUtf8("labelTitle"))
        self.horizontalLayout_2.addWidget(self.widget)
        self.debug = QtGui.QTextBrowser(self.centralwidget)
        self.debug.setGeometry(QtCore.QRect(60, 240, 261, 121))
        self.debug.setObjectName(_fromUtf8("debug"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.labelArtist.setText(_translate("MainWindow", "陶喆", None))
        self.labelAlbum.setText(_translate("MainWindow", "《黑色柳丁》2002", None))
        self.timeLabel.setText(_translate("MainWindow", "00:00:00", None))
        self.volumeSlider.setWhatsThis(_translate("MainWindow", "ss", None))
        self.labelTitle.setToolTip(_translate("MainWindow", "sssss", None))
        self.labelTitle.setText(_translate("MainWindow", "Fuck You", None))

from PyQt4 import phonon
import res_rc
