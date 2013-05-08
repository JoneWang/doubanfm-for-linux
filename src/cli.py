# coding: UTF-8
import shutil
from common import index_dir, tmp_dir, favicon, ms_to_hms, phonon_state_label, logger as l
from common.doubanfm import DoubanFM

import pygst
pygst.require('0.10')
import gst

import os
import sys    
import termios
import fcntl

def getch():
  fd = sys.stdin.fileno()

  oldterm = termios.tcgetattr(fd)
  newattr = termios.tcgetattr(fd)
  newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSANOW, newattr)

  oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
  fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

  try:        
    while 1:            
      try:
        c = sys.stdin.read(1)
        break
      except IOError: pass
  finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
  return c

class DoubanFMCli(object):
    def __init__(self, start_url=None):
        self.doubanfm = DoubanFM(start_url)
        self.player = gst.element_factory_make("playbin2", "player")
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)


    def on_message(self, bus, message):
        """docstring for on_message"""
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.next_song()
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            self.next_song()


    def _play_song(self):
        '''should be called by self.next_song() ONLY'''
        song = self.doubanfm.current_song
        self.player.set_property('uri',song.get('url'))
        self.player.set_state(gst.STATE_PLAYING)
        l.info(u'playing song: {sid} - {artist} - {title}'.format(**song))
        if int(song.get('like')) != 0:
            pass
        
    def play_toggle(self):
        song = self.doubanfm.current_song
        state = self.player.get_state()[1]
        if state == gst.STATE_PAUSED:
            self.player.set_state(gst.STATE_PLAYING)
        else:
            self.player.set_state(gst.STATE_PAUSED)

    def heart_song(self):
        song = self.doubanfm.current_song
        if int(song.get('like')) != 0:
            l.info(u'unhearted song: {sid} - {artist} - {title}'.format(**song))
            self.doubanfm.unheart_song()
        else:
            l.info(u'hearted song: {sid} - {artist} - {title}'.format(**song))
            self.doubanfm.heart_song()
    
    def trash_song(self):
        self.player.set_state(gst.STATE_NULL)
        song = self.doubanfm.current_song
        l.info(u'trash song: {sid} - {artist} - {title}'.format(**song))
        self.doubanfm.trash_song()
        self.next_song()

    def skip_song(self):
        self.player.set_state(gst.STATE_NULL)
        song = self.doubanfm.current_song
        l.info(u'skip song: {sid} - {artist} - {title}'.format(**song))
        self.doubanfm.skip_song()
        self.next_song()

    def next_song(self):
        self.doubanfm.next_song()
        self._play_song()

    def __del__(self):
        shutil.rmtree(tmp_dir)
        

if __name__ == '__main__':
    fm = DoubanFMCli()
    fm.next_song()

    hint = 'Command: Q[uit]\tn[ext]\tb[an]\tr[ed]\t[u]nred\tp[ause]\tP[lay]\th[elp]'
    print '😻  豆瓣FM'
    while True:
        c = getch()
        if c == 'Q':
            break
        elif c == 'n':
            fm.skip_song()
        elif c == 'b':
            fm.trash_song()
        elif c == 'r':
            fm.heart_song()
        elif c == 'u':
            fm.unheart_song()
        elif c == 'p' or c=='P':
            fm.play_toggle()
        elif c == 'h':
            print hint
