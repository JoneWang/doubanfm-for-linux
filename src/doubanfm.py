# coding: UTF-8
#
# 豆瓣FM
# 

import os
import sys
import urllib
import requests
import urlparse
import json
import pynotify
import time
import re
import pygst
pygst.require('0.10')
import gst
from util import getch
from share import set_skype_status
import tempfile

class DoubanFM(object):

    def __init__(self,debug=False,url=None):
        self._debug = debug
        self.ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
        self.COOKIE_PATH = os.path.join(self.ROOT_PATH, '.cookie')
        self.http_cookies = {}
        if os.path.exists(self.COOKIE_PATH):
            with open(self.COOKIE_PATH) as fh:
                cookies_text = fh.read().strip()
                try:
                    self.http_cookies = dict(cookie.split('=',1) for cookie in cookies_text.split('; ')) #TODO get uid
                except:
                    # TODO unlogin
                    pass
        
        self.douban_fm_host = 'douban.fm'
        self.douban_fm_hot_channel_path = '/j/explore/hot_channels'
        self.douban_fm_playlist_path = '/j/mine/playlist'
        self.douban_fm_channel_name= {0: u'私人兆赫', -3: u'红心兆赫', -8: u'红心兆赫 (TAG 版)'}
        self.douban_fm_default_params = {'type': 'n', 'sid': '', 'channel':0, 'pb': '192',
                'context':'', 'from':'mainsite', 'kbps':'192', 'r':'da01a52428'}
        
        self.http_session = requests.session(cookies=self.http_cookies)
        pre_request_url = url or 'http://%s/' % self.douban_fm_host
        res = self.http_session.get(pre_request_url)
        url_params =  urlparse.parse_qs(urlparse.urlparse(pre_request_url).query)
        start = url_params.get('start')
        context = url_params.get('context')
        cid = url_params.get('cid')
        if start:
            start = start[0]
            self.douban_fm_default_params['channel'] = start.split('g')[-1]
        if cid:
            cid = cid[0]
            self.douban_fm_default_params['channel'] = cid
        if context is not None:
            context = context[0]
            self.douban_fm_default_params['context'] = context

        self.player = gst.element_factory_make("playbin2", "player")
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

        self.current_channel = self.douban_fm_default_params['channel']

        self.current_playlist = []
        self.current_cur = -1

        self.timeout = 3
        pynotify.init ("icon-summary")
        self.tmp_dir = tempfile.mkdtemp('.cli.douban.fm')
    
    def __del__(self):
        self.player.set_state(gst.STATE_NULL)
        os.rmdir(self.tmp_dir) #TODO bug here,not called
    
    @property
    def current_song(self):
        if len(self.current_playlist) > 0 and self.current_cur > -1:
            return self.current_playlist[self.current_cur]
        else:
            print 'Ops...playlist is empty! exit'
            exit()
    
    def on_message(self, bus, message):
        """docstring for on_message"""
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.next_song()
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            self.next_song()

    def _get_playlist(self, params={}):
        params_tmp = self.douban_fm_default_params
        params_tmp.update(params)
        params_data = urllib.urlencode(params_tmp)
        url = '?'.join(('http://%s%s' % (self.douban_fm_host, self.douban_fm_playlist_path), params_data))
        res = self.http_session.get(url)
        #self.pr('set-cookie: %s' % res.headers.get('set-cookie'))
        if 'start="deleted"' in (res.headers.get('set-cookie') or ''):
            self.http_session.cookies.pop('start')
        cookies_text = '; '.join(['='.join(kv) for kv in self.http_session.cookies.items()])
        with open(self.COOKIE_PATH,'w') as fh:
            fh.write(cookies_text)
        #self.pr('current cookies: %s' % self.http_session.cookies.items())
        self.pr('_get_playlist: %s' % url)
        res_json = json.loads(res.text)
        if int(res_json.get('r')) == 0:
            return res_json['song']
        elif int(res_json.get('r')) == 1:
            print 'error: %s' % res_json['err']
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
        current_song = self.current_song
        i_title = current_song.get('title')
        i_artist = current_song.get('artist')
        i_album = current_song.get('album')
        i_albumtitle = current_song.get('albumtitle')
        i_islike = int(current_song.get('like')) == 1
        i_url = 'http://{0}/?start={1}g{2}g{3}&cid={3}'.format(self.douban_fm_host,
                    current_song.get('sid'), 
                    current_song.get('ssid'), 
                    self.current_channel)
        i_cover_path = "/%s/cover.%s.jpg" % (self.tmp_dir,current_song.get('sid'))
        urllib.urlretrieve(current_song.get('picture'),i_cover_path)

        playing_info = '▶  %s - %s %s [%s](%s)' % (i_artist, i_title, '♥ '  if i_islike else '',i_albumtitle, i_url)
        terminal_title = "\x1b]2;▶  %s - %s\x07" % (i_artist,i_title)
        sns_info = '♪ 正在豆瓣FM#%s#收听: %s - %s %s' % (self.douban_fm_channel_name.get(self.current_channel, 'DJ兆赫') ,
                i_artist, i_title, i_url)
        print playing_info
        print terminal_title
        n = pynotify.Notification(i_artist, i_title,i_cover_path)
        n.show()
        set_skype_status(sns_info)
        # XXX donot print playing information on resume after pause

    def pause(self):
        """暂停"""
        self.player.set_state(gst.STATE_PAUSED)

    def next_song(self):
        """自动续播"""
        self.player.set_state(gst.STATE_NULL)
        
        if self.current_cur == -1 or self.current_cur >= len(self.current_playlist) - 1:
            self.current_playlist.extend(self._get_playlist())
        self.current_cur += 1

        current_song = self.current_song
        self.player.set_property('uri',current_song['url'])
        self.play()
        
    def pass_song(self): 
        """人为跳过"""
        self.player.set_state(gst.STATE_NULL)
        current_song = self.current_song
        self.current_playlist = self._get_playlist(params={'type':'p','sid': current_song.get('sid')})
        self.current_cur = 0
        current_song = self.current_song
        self.player.set_property('uri',current_song['url'])

        self.play()

    def ban_song(self):
        """垃圾桶"""
        self.player.set_state(gst.STATE_NULL)
        current_song = current_song
        self.current_playlist = self._get_playlist(params={'type':'b','sid': current_song.get('sid')})
        self.current_cur = 0
        current_song = self.current_playlist[self.current_cur]
        self.player.set_property('uri',current_song['url'])
        self.play()

    def red_song(self):
        """红心"""
        current_song = self.current_song
        if int(current_song.get('like')) != 1:
            self.current_playlist.extend(self._get_playlist(params={'type':'r','sid': current_song.get('sid')}))
            print '<3 %s' % current_song.get('title')
            self.current_song['like'] = 1


    def unred_song(self):
        """红心"""
        current_song = self.current_song
        if int(current_song.get('like')) != 0:
            self.current_playlist.extend(self._get_playlist(params={'type':'u','sid': current_song.get('sid')}))
            print '</3  %s' % current_song.get('title')
            self.current_song['like'] = 0
            #self.current_cur += 1
            #current_song = self.current_playlist[self.current_cur]
            #self.player.set_property('uri',current_song['url'])
    
    def pr(self, msg):
        if self._debug:
            print '-' * 20
            print msg



if __name__ == '__main__':
    argv = sys.argv
    url = None
    if len(argv) >= 2:
        url = argv[1]
    fm = DoubanFM(debug=False, url=url)
    hint = 'Command: Q[uit]\tn[ext]\tr[ed]\t[u]nred\tp[ause]\tP[lay]\th[elp]'
    print hint
    fm.play()
    while True:
        c = getch()
        if c == 'Q':
            set_skype_status('')
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
        elif c == 'h':
            print hint
