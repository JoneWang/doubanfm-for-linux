# coding: UTF-8

import os
import urllib
import requests
import json
import pynotify
import sys
import time
import re
import pygst
pygst.require('0.10')
import gst
from util import getch
from share import set_skype_status

class DoubanFM(object):

    def __init__(self,debug=False):
        self.debug = debug
        self.ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
        self.COOKIE_PATH = os.path.join(self.ROOT_PATH, '.cookie')
        self.http_headers = {}
        if os.path.exists(self.COOKIE_PATH):
            with open(self.COOKIE_PATH) as fh:
                http_cookie = fh.read().strip()
                self.http_headers['Cookie'] = http_cookie #TODO get uid
        
        self.douban_fm_host = 'douban.fm'
        self.douban_fm_hot_channel_path = '/j/explore/hot_channels'
        self.douban_fm_playlist_path = '/j/mine/playlist'
        self.douban_fm_private_channels_dict = {0: u'私人兆赫', -3: u'红心兆赫', -8: u'红心兆赫 (TAG 版)'}
        self.douban_fm_default_params = {'type': 'n', 'sid': '', 'channel':0, 'pb': '192', 'from':'mainsite', 'kbps':'192', 'r':'da01a52428'}

        self.player = gst.element_factory_make("playbin", "player")
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

        self.current_uid = 0
        self.current_channel = 0
        self.current_sid = 0
        self.current_playlist = []
        self.current_cur = 0

        self.timeout = 3
    
    def __del__(self):
        player.set_state(gst.STATE_NULL)

    def on_message(self, bus, message):
        """docstring for on_message"""
        t = message.type
        if t == gst.MESSAGE_EOS:
            player.set_state(gst.STATE_NULL)
            self.next_song()
        elif t == gst.MESSAGE_ERROR:
            player.set_state(gst.STATE_NULL)
            self.next_song()

    def _get_playlist(self, params={}):
        params_tmp = self.douban_fm_default_params
        params_tmp.update(params)
        params_data = urllib.urlencode(params_tmp)
        url = '?'.join(('http://%s%s' % (self.douban_fm_host, self.douban_fm_playlist_path), params_data))
        res = requests.get(url, headers=self.http_headers)
        if self.debug:
            print '_get_playlist: %s' % url
        res_json = json.loads(res.text)
        if res_json.get('r') == 0:
            return res_json['song']
        else:
            print 'empty on %s' % url
            return []
    
    def play(self):
        """播放"""
        if len(self.current_playlist) == 0:
            # 初始化和之前各种行为_get_playlist 都没获取到歌曲才会进到这里
            if self.timeout > 0:
                self.next_song()
                self.timeout -= 1
            else:
                print 'timeout on loading playlist, exit'
                sys.exit(1)
            return 
        self.player.set_state(gst.STATE_PLAYING)
        current_song = self.current_playlist[self.current_cur]
        #sys.stdout.flush()
        #sys.stdout.write('%s - %s\r' % (current_song.get('artist'),current_song.get('title'), ))
        print '%s - %s\r' % (current_song.get('artist'),current_song.get('title'), )
        set_skype_status('♪ 正在豆瓣FM#%s#上收听: %s - %s' % (self.douban_fm_private_channels_dict[self.current_channel] ,\
                current_song.get('artist'), current_song.get('title')))
        # TODO print play information

    def pause(self):
        """暂停"""
        self.player.set_state(gst.STATE_PAUSED)

    def next_song(self):
        """自动续播"""
        self.player.set_state(gst.STATE_NULL)
        if self.current_cur >= len(self.current_playlist):
            self.current_playlist.extend(self._get_playlist())
        self.current_cur += 1
        current_song = self.current_playlist[self.current_cur]
        self.player.set_property('uri',current_song['url'])
        self.play()
        
    def pass_song(self): 
        """人为跳过"""
        self.player.set_state(gst.STATE_NULL)
        current_song = self.current_playlist[self.current_cur]
        self.current_playlist = self._get_playlist(params={'type':'p','sid': current_song.get('sid')})
        self.current_cur = 0
        current_song = self.current_playlist[self.current_cur]
        self.player.set_property('uri',current_song['url'])

        self.play()

    def ban_song(self):
        """垃圾桶"""
        self.player.set_state(gst.STATE_NULL)
        current_song = self.current_playlist[self.current_cur]
        self.current_playlist = self._get_playlist(params={'type':'b','sid': current_song.get('sid')})
        self.current_cur = 0
        current_song = self.current_playlist[self.current_cur]
        self.player.set_property('uri',current_song['url'])
        self.play()

    def red_song(self):
        """红心"""
        current_song = self.current_playlist[self.current_cur]
        if current_song.get('like') != 1:
            self.current_playlist.extend(self._get_playlist(params={'type':'r','sid': current_song.get('sid')}))
            print 'reded %s' % current_song.get('title')


    def unred_song(self):
        """红心"""
        current_song = self.current_playlist[self.current_cur]
        if current_song.get('like') != 0:
            self.current_playlist.extend(self._get_playlist(params={'type':'u','sid': current_song.get('sid')}))
            print 'unreded %s' % current_song.get('title')
            #self.current_cur += 1
            #current_song = self.current_playlist[self.current_cur]
            #self.player.set_property('uri',current_song['url'])



if __name__ == '__main__':
    fm = DoubanFM(debug=True)
    fm.play()
    while True:
        c = getch()
        if c == 'Q':
            break
        elif c == 'n':
            fm.pass_song()
        elif c == 'r':
            fm.red_song()
        elif c == 'u':
            fm.unred_song()
        elif c == 'p':
            fm.pause()
        elif c == 'P':
            fm.play()

