# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/player.ui'
#
# Created: Wed May  8 13:44:17 2013
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
        MainWindow.resize(510, 245)
        MainWindow.setMinimumSize(QtCore.QSize(510, 245))
        MainWindow.setMaximumSize(QtCore.QSize(510, 245))
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(_fromUtf8("background-color: rgba(255,255,255);"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(510, 245))
        self.centralwidget.setMaximumSize(QtCore.QSize(510, 245))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.leftwidget = QtGui.QWidget(self.centralwidget)
        self.leftwidget.setMinimumSize(QtCore.QSize(245, 245))
        self.leftwidget.setMaximumSize(QtCore.QSize(245, 245))
        self.leftwidget.setObjectName(_fromUtf8("leftwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.leftwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonCover = QtGui.QPushButton(self.leftwidget)
        self.pushButtonCover.setMaximumSize(QtCore.QSize(245, 245))
        self.pushButtonCover.setBaseSize(QtCore.QSize(245, 245))
        self.pushButtonCover.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonCover.setStyleSheet(_fromUtf8("border: none;\n"
"outline: none;"))
        self.pushButtonCover.setText(_fromUtf8(""))
        self.pushButtonCover.setIconSize(QtCore.QSize(245, 245))
        self.pushButtonCover.setObjectName(_fromUtf8("pushButtonCover"))
        self.horizontalLayout.addWidget(self.pushButtonCover)
        self.horizontalLayout_2.addWidget(self.leftwidget)
        self.rightwidget = QtGui.QWidget(self.centralwidget)
        self.rightwidget.setMinimumSize(QtCore.QSize(265, 245))
        self.rightwidget.setMaximumSize(QtCore.QSize(265, 245))
        self.rightwidget.setObjectName(_fromUtf8("rightwidget"))
        self.gridLayout = QtGui.QGridLayout(self.rightwidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(7, 25, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(170, 5, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 8, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(17, 25, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem3, 4, 1, 1, 2)
        self.labelAlbum = QtGui.QLabel(self.rightwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelAlbum.sizePolicy().hasHeightForWidth())
        self.labelAlbum.setSizePolicy(sizePolicy)
        self.labelAlbum.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Sans Serif"))
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.labelAlbum.setFont(font)
        self.labelAlbum.setStyleSheet(_fromUtf8("color: \'#333\';\n"
""))
        self.labelAlbum.setObjectName(_fromUtf8("labelAlbum"))
        self.gridLayout.addWidget(self.labelAlbum, 3, 1, 1, 2)
        self.timeLabel = QtGui.QLabel(self.rightwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeLabel.sizePolicy().hasHeightForWidth())
        self.timeLabel.setSizePolicy(sizePolicy)
        self.timeLabel.setMinimumSize(QtCore.QSize(0, 10))
        self.timeLabel.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Sans Serif"))
        font.setPointSize(9)
        self.timeLabel.setFont(font)
        self.timeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.timeLabel.setObjectName(_fromUtf8("timeLabel"))
        self.gridLayout.addWidget(self.timeLabel, 7, 1, 1, 2)
        self.seekSlider = phonon.Phonon.SeekSlider(self.rightwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.seekSlider.sizePolicy().hasHeightForWidth())
        self.seekSlider.setSizePolicy(sizePolicy)
        self.seekSlider.setMinimumSize(QtCore.QSize(150, 7))
        self.seekSlider.setMaximumSize(QtCore.QSize(16777215, 7))
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
"     margin: -2px 0;\n"
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
        self.gridLayout.addWidget(self.seekSlider, 6, 1, 1, 2)
        self.labelArtist = QtGui.QLabel(self.rightwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelArtist.sizePolicy().hasHeightForWidth())
        self.labelArtist.setSizePolicy(sizePolicy)
        self.labelArtist.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.labelArtist.setFont(font)
        self.labelArtist.setStyleSheet(_fromUtf8("color: \'#333\';\n"
""))
        self.labelArtist.setObjectName(_fromUtf8("labelArtist"))
        self.gridLayout.addWidget(self.labelArtist, 2, 1, 1, 2)
        self.volumeSlider = phonon.Phonon.VolumeSlider(self.rightwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.volumeSlider.sizePolicy().hasHeightForWidth())
        self.volumeSlider.setSizePolicy(sizePolicy)
        self.volumeSlider.setMinimumSize(QtCore.QSize(50, 10))
        self.volumeSlider.setWhatsThis(_fromUtf8(""))
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
        self.gridLayout.addWidget(self.volumeSlider, 8, 2, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 70, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem4, 10, 1, 1, 2)
        self.labelTitle = QtGui.QLabel(self.rightwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTitle.sizePolicy().hasHeightForWidth())
        self.labelTitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.labelTitle.setFont(font)
        self.labelTitle.setWhatsThis(_fromUtf8(""))
        self.labelTitle.setStyleSheet(_fromUtf8("color: \'#9dd6c5\';\n"
""))
        self.labelTitle.setObjectName(_fromUtf8("labelTitle"))
        self.gridLayout.addWidget(self.labelTitle, 5, 1, 1, 2)
        self.pushButtonToggle = QtGui.QPushButton(self.rightwidget)
        self.pushButtonToggle.setMinimumSize(QtCore.QSize(28, 28))
        self.pushButtonToggle.setMaximumSize(QtCore.QSize(28, 28))
        self.pushButtonToggle.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonToggle.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButtonToggle.setStyleSheet(_fromUtf8("background: url(:/player/pause.png) no-repeat center;\n"
"border: none;\n"
"outline: none;\n"
"background-color: \'#9dd6c5\';\n"
"border-radius: 1px;\n"
""))
        self.pushButtonToggle.setText(_fromUtf8(""))
        self.pushButtonToggle.setAutoDefault(True)
        self.pushButtonToggle.setObjectName(_fromUtf8("pushButtonToggle"))
        self.gridLayout.addWidget(self.pushButtonToggle, 1, 2, 1, 1)
        self.horizontalLayoutControl = QtGui.QHBoxLayout()
        self.horizontalLayoutControl.setSpacing(22)
        self.horizontalLayoutControl.setContentsMargins(50, 0, 0, 0)
        self.horizontalLayoutControl.setObjectName(_fromUtf8("horizontalLayoutControl"))
        self.pushButtonHeart = QtGui.QPushButton(self.rightwidget)
        self.pushButtonHeart.setMinimumSize(QtCore.QSize(28, 28))
        self.pushButtonHeart.setMaximumSize(QtCore.QSize(28, 28))
        self.pushButtonHeart.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonHeart.setStyleSheet(_fromUtf8("border-image: url(:/player/heart.png);\n"
"border: none;\n"
"outline: none;"))
        self.pushButtonHeart.setText(_fromUtf8(""))
        self.pushButtonHeart.setAutoDefault(True)
        self.pushButtonHeart.setFlat(True)
        self.pushButtonHeart.setObjectName(_fromUtf8("pushButtonHeart"))
        self.horizontalLayoutControl.addWidget(self.pushButtonHeart)
        self.pushButtonTrash = QtGui.QPushButton(self.rightwidget)
        self.pushButtonTrash.setMinimumSize(QtCore.QSize(28, 28))
        self.pushButtonTrash.setMaximumSize(QtCore.QSize(28, 28))
        self.pushButtonTrash.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonTrash.setStyleSheet(_fromUtf8("border-image: url(:/player/trash.png);\n"
"border: none;\n"
"outline: none;"))
        self.pushButtonTrash.setText(_fromUtf8(""))
        self.pushButtonTrash.setAutoDefault(True)
        self.pushButtonTrash.setFlat(True)
        self.pushButtonTrash.setObjectName(_fromUtf8("pushButtonTrash"))
        self.horizontalLayoutControl.addWidget(self.pushButtonTrash)
        self.pushButtonSkip = QtGui.QPushButton(self.rightwidget)
        self.pushButtonSkip.setMinimumSize(QtCore.QSize(28, 28))
        self.pushButtonSkip.setMaximumSize(QtCore.QSize(28, 28))
        self.pushButtonSkip.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonSkip.setStyleSheet(_fromUtf8("border-image: url(:/player/skip.png);\n"
"border: none;\n"
"outline: none;"))
        self.pushButtonSkip.setText(_fromUtf8(""))
        self.pushButtonSkip.setAutoDefault(True)
        self.pushButtonSkip.setFlat(True)
        self.pushButtonSkip.setObjectName(_fromUtf8("pushButtonSkip"))
        self.horizontalLayoutControl.addWidget(self.pushButtonSkip)
        self.pushButtonShare = QtGui.QPushButton(self.rightwidget)
        self.pushButtonShare.setMinimumSize(QtCore.QSize(28, 28))
        self.pushButtonShare.setMaximumSize(QtCore.QSize(28, 28))
        self.pushButtonShare.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonShare.setStyleSheet(_fromUtf8("border-image: url(:/player/share.png);\n"
"border: none;\n"
"outline: none;"))
        self.pushButtonShare.setText(_fromUtf8(""))
        self.pushButtonShare.setObjectName(_fromUtf8("pushButtonShare"))
        self.horizontalLayoutControl.addWidget(self.pushButtonShare)
        self.gridLayout.addLayout(self.horizontalLayoutControl, 11, 1, 1, 2)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 12, 1, 1, 2)
        self.horizontalLayout_2.addWidget(self.rightwidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.labelAlbum.setText(_translate("MainWindow", "《黑色柳丁》2002", None))
        self.timeLabel.setText(_translate("MainWindow", "- 00:00", None))
        self.labelArtist.setText(_translate("MainWindow", "陶喆", None))
        self.labelTitle.setToolTip(_translate("MainWindow", "sssss", None))
        self.labelTitle.setText(_translate("MainWindow", "Fuck You", None))

from PyQt4 import phonon
import res_rc
