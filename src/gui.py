# coding: UTF-8

# Douban FM GUI
#

import os
import sys
import shutil
import urllib

import webbrowser

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QPixmap, QIcon, QLabel, QWidgetAction, qApp
from PyQt4.QtCore import QSize
from PyQt4.phonon import Phonon

from ui.player import Ui_MainWindow, _fromUtf8
from common import index_dir, tmp_dir, favicon, phonon_state_label, \
        logger as l, ms_to_hms, async, is_unity
from common.doubanfm import DoubanFM

class GUIState:
    (Playing, Paused, Heart, Hearted) = range(4)

class DoubanFMGUI(QtGui.QMainWindow):
    def __init__(self, parent=None, start_url=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow() 
        self.ui.setupUi(self)
        self.ui.seekSlider.setIconVisible(False)
        self.ui.volumeSlider.setMuteVisible(False)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setup_player_ui()
        self.total_time = None
        self.doubanfm = DoubanFM(start_url, debug=False)
        self.connect(self.ui.pushButtonHeart, QtCore.SIGNAL('clicked()'), self.heart_song)
        self.connect(self.ui.pushButtonTrash, QtCore.SIGNAL('clicked()'), self.trash_song)
        self.connect(self.ui.pushButtonSkip, QtCore.SIGNAL('clicked()'), self.skip_song)
        self.connect(self.ui.pushButtonToggle, QtCore.SIGNAL('clicked()'), self.play_toggle)
        self.connect(self.ui.pushButtonCover, QtCore.SIGNAL('clicked()'), self.on_click_cover)
        self.connect(self.ui.pushButtonShare, QtCore.SIGNAL('clicked()'), self.on_click_share)
        self.connect(self, QtCore.SIGNAL('cover_image_ready()'), self.__set_cover)
        l.info('DoubanFM init')
        self.next_song()

    def setup_player_ui(self):
        # Setup phonon player
        self.mediaObject = Phonon.MediaObject(self)
        self.mediaObject.setTickInterval(500)
        self.mediaObject.tick.connect(self.tick)
        #self.mediaObject.finished.connect(self.finished)
        self.mediaObject.stateChanged.connect(self.catchStateChanged)
        self.mediaObject.totalTimeChanged.connect(self._set_total_time)

        # bind AudioOutput with MediaObject
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        Phonon.createPath(self.mediaObject, self.audioOutput)

        # Setup the seek slider
        self.ui.seekSlider.setMediaObject(self.mediaObject)

        # Setup the volume slider
        self.ui.volumeSlider.setAudioOutput(self.audioOutput)

    def set_ui_state(self, state):
        #TODO: refactor
        if state == GUIState.Playing:
            self.ui.pushButtonToggle.setStyleSheet(_fromUtf8("background: url(:/player/pause.png) no-repeat center;\nborder: none;\n outline: none;\n background-color: '#9dd6c5';"))
        elif state == GUIState.Paused:
            self.ui.pushButtonToggle.setStyleSheet(_fromUtf8("background: url(:/player/play.png) no-repeat center;\nborder: none;\n outline: none;\n background-color: '#9dd6c5';"))
        elif state == GUIState.Heart:
            self.ui.pushButtonHeart.setStyleSheet('border-image: url(:/player/heart.png);\nborder: none;\noutline: none;')
        elif state == GUIState.Hearted:
            self.ui.pushButtonHeart.setStyleSheet('border-image: url(:/player/hearted.png);\nborder: none;\noutline: none;')

    def leaveEvent(self, e):
        # the real lose focus event, WTF
        # http://harmattan-dev.nokia.com/docs/library/html/qt4/qwidget.html#leaveEvent
        self.hide()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.hide()


    def on_click_cover(self):
        song = self.doubanfm.current_song
        subject_url = u'http://music.douban.com{album}'.format(**song)
        self.open_url(subject_url)

    def on_click_share(self):
        song = self.doubanfm.current_song
        self.open_url(song.get('song_url'))
        
    def tick(self, time):
        if self.total_time is None:
            return
        time_remaining = self.total_time - time
        h, m, s = ms_to_hms(time_remaining)
        if h == 0:
            time_text = '%d:%02d' % (m, s)
        else:
            time_text = '%d:%02d:%02d' % (h, m, s)

        if time_remaining > 0:
            time_text = '-%s' % time_text
        self.ui.timeLabel.setText(time_text)

    def _set_total_time(self, time):
        self.total_time = time
        
    def catchStateChanged(self, new_state, old_state):
        ''' 
        possible state sequences:
        [init]: loading -> [next]
        [next]: stop -> paused -> playing -> stop(*)
        [skip],[trash]: playing -> paused -> stop -> pause -> playing(*)
        '''
        l.debug(u'old_state: {0}, new_state: {1}'.format(phonon_state_label.get(old_state), phonon_state_label.get(new_state)))
        #http://harmattan-dev.nokia.com/docs/library/html/qt4/phonon.html
        if new_state == Phonon.PlayingState:
            self.set_ui_state(GUIState.Playing)
        elif new_state == Phonon.PausedState:
            self.set_ui_state(GUIState.Paused)
        elif new_state == Phonon.StoppedState:
            if old_state == Phonon.PlayingState:#auto next song
                self.next_song()
        elif new_state == Phonon.ErrorState:
            l.error('error while playing back')
            self.next_song()

    def _play_song(self):
        '''should be called by self.next_song() ONLY'''
        song = self.doubanfm.current_song
        l.info(u'playing song: {sid} - {artist} - {title}'.format(**song))
        self.ui.labelAlbum.setText(u'<{0}> {1}'.format(song.get('albumtitle'), song.get('public_time') or ''))
        self.ui.labelTitle.setText(song.get('title'))
        self.ui.labelTitle.setToolTip(song.get('title'))
        self.ui.labelArtist.setText(song.get('artist'))
        if int(song.get('like')) != 0:
            self.set_ui_state(GUIState.Hearted)
        else:
            self.set_ui_state(GUIState.Heart)

        self.mediaObject.setCurrentSource(Phonon.MediaSource(song.get('url')))
        self.mediaObject.play()
        self.__down_cover()

        from share import now_playing
        now_playing(song,channel_id=self.doubanfm.channel_id,channel_name=self.doubanfm.channel_name)
    
    @async
    def open_url(self, url):
        webbrowser.open_new_tab(url)

    @async
    def __down_cover(self):
        song = self.doubanfm.current_song
        self._local_cover_path = os.path.join(tmp_dir, 'cover-%s.jpg' % song.get('sid'))
        urllib.urlretrieve(song.get('picture').replace('mpic', 'lpic'), self._local_cover_path)
        self.emit(QtCore.SIGNAL('cover_image_ready()'))

    def __set_cover(self):
        pixmap = QPixmap(self._local_cover_path)
        pixmap = pixmap.scaled(self.ui.pushButtonCover.iconSize(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
        pixmap_size = self.ui.pushButtonCover.iconSize()
        pixmap = pixmap.copy(0,0,pixmap_size.width(), pixmap_size.height())
        cover = QIcon(pixmap)
        self.ui.pushButtonCover.setIcon(cover)


    def play_toggle(self):
        song = self.doubanfm.current_song
        ns = self.mediaObject.state()
        if ns == Phonon.PlayingState:
            self.mediaObject.pause()
        elif ns == Phonon.PausedState:
            self.mediaObject.play()

    def heart_song(self):
        song = self.doubanfm.current_song
        if int(song.get('like')) != 0:
            l.info(u'unhearted song: {sid} - {artist} - {title}'.format(**song))
            self.set_ui_state(GUIState.Heart)
            self.doubanfm.unheart_song()
        else:
            l.info(u'hearted song: {sid} - {artist} - {title}'.format(**song))
            self.set_ui_state(GUIState.Hearted)
            self.doubanfm.heart_song()
    
    def trash_song(self):
        song = self.doubanfm.current_song
        l.info(u'trash song: {sid} - {artist} - {title}'.format(**song))
        self.doubanfm.trash_song()
        self.next_song()

    def skip_song(self):
        song = self.doubanfm.current_song
        l.info(u'skip song: {sid} - {artist} - {title}'.format(**song))
        self.doubanfm.skip_song()
        self.next_song()

    def next_song(self):
        self.doubanfm.next_song()
        self._play_song()

    def __del__(self):
        print 'DoubanFM safely exit'
        self.mediaObject.stop()

class SystemTrayApp(QtGui.QSystemTrayIcon):
    def __init__(self, parent, width, height):
        QtGui.QSystemTrayIcon.__init__(self, parent)
        self.setIcon(QtGui.QIcon(favicon))
        self.screen_size = (width, height)
        start_url = None
        if len(sys.argv) >= 2:
            start_url = sys.argv[1]

        self.main_window = DoubanFMGUI(start_url=start_url)

        self.rightMenu = QtGui.QMenu(parent)
        username = self.main_window.doubanfm.username
        channel_name = self.main_window.doubanfm.channel_name
        icon = self.rightMenu.addAction("Douban FM for Linux")
        channel = self.rightMenu.addAction('%s MHz' % channel_name)
        self.connect(icon,QtCore.SIGNAL('triggered()'),self.toggle_main_window)

        self.rightMenu.addAction(u'@{0}'.format((username or u'anonymous')))
        app_exit = self.rightMenu.addAction("Exit")
        self.connect(app_exit,QtCore.SIGNAL('triggered()'),self.app_exit)

        self.setContextMenu(self.rightMenu)
        self.activated.connect(self.click_trap)

    def click_trap(self, reason):
        #  http://t.cn/zTQz8cV 
        # trigger is not supported in unity
        if reason == QtGui.QSystemTrayIcon.Trigger: 
            self.toggle_main_window()

    def toggle_main_window(self):
        if self.main_window.isHidden():
            mouse_x = QtGui.QCursor.pos().x()
            mouse_y = QtGui.QCursor.pos().y()
            window_h = self.main_window.minimumHeight()
            window_w = self.main_window.minimumWidth()
            if mouse_x + window_w > self.screen_size[0]:
                mouse_x -= window_w
            if mouse_y + window_h > self.screen_size[1]:
                mouse_y -= window_h
            # XXX naive fix of window position for unity
            if is_unity:
                mouse_y -= mouse_y
            self.main_window.setGeometry(mouse_x, mouse_y, window_w, window_h)
            self.main_window.show()
            self.main_window.setFocus()
        else:
            self.main_window.hide()

    def app_exit(self):
        shutil.rmtree(tmp_dir)
        return qApp.quit()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("Douban FM")
    main_window = DoubanFMGUI()
    main_window.show()
    sys.exit(app.exec_())
