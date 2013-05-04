#!/usr/bin/env python2
import os
import sys
import urllib
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QPixmap, QIcon
from PyQt4.QtCore import QSize
from PyQt4.phonon import Phonon
from ui.player import Ui_MainWindow, _fromUtf8

from doubanfm import DoubanFM

class DoubanFMGUI(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow() 
        self.ui.setupUi(self)
        self.setup_gui()
        self.ui.seekSlider.setIconVisible(False)
        self.ui.volumeSlider.setMuteVisible(False)
        self.doubanfm = DoubanFM()
        print self.doubanfm.username
        self.connect(self.ui.pushButtonHeart, QtCore.SIGNAL('clicked()'), self.heart_song)
        self.connect(self.ui.pushButtonSkip, QtCore.SIGNAL('clicked()'), self.skip_song)
        self.connect(self.ui.pushButtonToggle, QtCore.SIGNAL('clicked()'), self.pause_toggle)

        print 'init'
        self.next_song()

    def setup_gui(self):
        # Setup phonon player
        self.mediaObject = Phonon.MediaObject(self)
        self.mediaObject.setTickInterval(100)
        self.mediaObject.tick.connect(self.tick)
        #self.mediaObject.finished.connect(self.finished)
        self.mediaObject.stateChanged.connect(self.catchStateChanged)
        #self.mediaObject.totalTimeChanged.connect(self.totalTime)

        # bind AudioOutput with MediaObject
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        Phonon.createPath(self.mediaObject, self.audioOutput)

        # Setup the seek slider
        self.ui.seekSlider.setMediaObject(self.mediaObject)

        # Setup the volume slider
        self.ui.volumeSlider.setAudioOutput(self.audioOutput)

        # Dont show the GUI if called that way AKA cli mode
        #if not self.disableGui:

    def msToHms(self, timeMs):
        """Convert timeMS in milliseconds to h m s format"""
        s = timeMs / 1000
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return h, m, s


    def tick(self, time):
        """Catch the signal from the media object and update the time"""
        # time is received as time in milliseconds, convert to h m s
        h, m, s = self.msToHms(time)
        self.ui.timeLabel.setText('%02d:%02d:%02d' %(h, m, s))

    def catchStateChanged(self, new_state, old_state):
        #http://harmattan-dev.nokia.com/docs/library/html/qt4/phonon.html
        if new_state == Phonon.PlayingState:
            self.ui.pushButtonToggle.setStyleSheet(_fromUtf8("background: url(:/player/pause.png) no-repeat center;\nborder: none;\n outline: none;\n background-color: '#9dd6c5';"))
        elif new_state == Phonon.PausedState:
            self.ui.pushButtonToggle.setStyleSheet(_fromUtf8("background: url(:/player/play.png) no-repeat center;\nborder: none;\n outline: none;\n background-color: '#9dd6c5';"))
        elif new_state == Phonon.StoppedState:
            self.next_song()
        elif new_state == Phonon.ErrorState:
            print('Error playing back file')
            self.quit()
        print '~' * 40
        print 'new_state:', new_state
        print '~' * 40

    def play_song(self):
        song = self.doubanfm.current_song
        url = song.get('url')
        self.ui.labelAlbum.setText(u'<{0}> {1}'.format(song.get('albumtitle'), song.get('public_time')))
        self.ui.labelTitle.setText(song.get('title'))
        self.ui.labelTitle.setToolTip(song.get('title'))
        self.ui.labelArtist.setText(song.get('artist'))
        urllib.urlretrieve(song.get('picture').replace('mpic', 'lpic'),'/tmp/cover.jpg')
        cover = QIcon('/tmp/cover.jpg')

        self.ui.pushButtonCover.setIcon(cover)
        self.ui.pushButtonCover.setIconSize(QSize(200,200))
        if int(song.get('like')) != 0:
            s = 'hearted'
        else:
            s = 'heart'
        self.ui.pushButtonHeart.setStyleSheet('border-image: url(:/player/%s.png);\nborder: none;\noutline: none;' % s)
        self.ui.debug.setText(str(song))
        
        self.mediaObject.setCurrentSource(Phonon.MediaSource(url))
        self.mediaObject.play()

    def skip_song(self):
        song = self.doubanfm.pass_song()
        self.play_song()


    def pause_toggle(self):
        ns = self.mediaObject.state()
        if ns == Phonon.PlayingState:
            self.mediaObject.pause()
        elif ns == Phonon.PausedState:
            self.mediaObject.play()

    def heart_song(self):
        song = self.doubanfm.current_song
        old_state = song.get('like')
        if old_state != 0:
            self.doubanfm.unred_song()
            self.ui.pushButtonHeart.setStyleSheet('border-image: url(:/player/heart.png);\nborder: none;\noutline: none;')
        else:
            self.doubanfm.red_song()
            self.ui.pushButtonHeart.setStyleSheet('border-image: url(:/player/hearted.png);\nborder: none;\noutline: none;')

    def next_song(self):
        self.doubanfm.next_song()
        self.play_song()
        

if __name__ == "__main__":
    print 'start up'
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("Douban FM")
    doubanfm = DoubanFMGUI()
    doubanfm.show()
    sys.exit(app.exec_())
    print 'exit'
