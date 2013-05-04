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
import time
import re
from util import getch
#from share import set_skype_status, notify
from plugin import test_filter
import tempfile
import BeautifulSoup



class DoubanFM(object):

    def __init__(self,debug=False,url=None):
        self._debug = debug
        self.ROOT_PATH = os.path.abspath(os.path.dirname(__file__) + '/../')
        self.COOKIE_PATH = os.path.join(self.ROOT_PATH, '.cookie')
        self.http_cookies = {}
        if os.path.exists(self.COOKIE_PATH):
            with open(self.COOKIE_PATH) as fh:
                cookies_text = fh.read().strip()
                try:
                    self.http_cookies = dict(cookie.split('=',1) for cookie in cookies_text.split('; '))
                except:
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

        #print '😻  豆瓣FM', 
        try:
            soup = BeautifulSoup.BeautifulSoup(res.text)
            self.username = soup.find(id='user_name').text
            #print '@%s' % self.username
        except:
            self.username = None
            #print '@anonymous'

        url_params =  urlparse.parse_qs(urlparse.urlparse(pre_request_url).query)
        start = url_params.get('start')
        context = url_params.get('context')
        cid = url_params.get('cid')
        if start:
            start = start[0]
            self.douban_fm_default_params['channel'] = start.split('g')[-1]
        if cid:
            cid = cid[0]
            self.douban_fm_default_params['channel'] = int(cid)
        if context is not None:
            context = context[0]
            self.douban_fm_default_params['context'] = context

        self.current_channel = self.douban_fm_default_params['channel']

        self.current_playlist = []
        self.current_cur = -2

        self.timeout = 3
        
        self.tmp_dir = tempfile.mkdtemp('.cli.douban.fm')
    
    def __del__(self):
        os.rmdir(self.tmp_dir) #TODO bug here,not called
    
    @property
    def current_song(self):
        if len(self.current_playlist) > 0 and self.current_cur > -2:
            return self.current_playlist[self.current_cur]
        else:
            print 'Ops...playlist is empty! exit'
            sys.exit()

    def _get_playlist(self, params={}):
        params_tmp = self.douban_fm_default_params
        params_tmp.update(params)
        params_data = urllib.urlencode(params_tmp)
        url = '?'.join(('http://%s%s' % (self.douban_fm_host, self.douban_fm_playlist_path), params_data))
        res = self.http_session.get(url)
        if 'start="deleted"' in (res.headers.get('set-cookie') or ''):
            self.http_session.cookies.pop('start')
        cookies_text = '; '.join(['='.join(kv) for kv in self.http_session.cookies.items()])
        with open(self.COOKIE_PATH,'w') as fh:
            fh.write(cookies_text)
        res_json = json.loads(res.text)
        if int(res_json.get('r')) == 0:
            return res_json['song']
        elif int(res_json.get('r')) == 1:
            #print 'error: %s' % res_json['err']
            return []
       
    def next_song(self):
        """自动续播"""
        if self.current_cur == -2 or self.current_cur >= len(self.current_playlist) - 2:
            self.current_playlist.extend(self._get_playlist())
        self.current_cur += 1
        
    def skip_song(self): 
        """人为跳过"""
        self.current_playlist = self._get_playlist(params={'type':'p','sid': self.current_song.get('sid')})
        self.current_cur = -1

    def trash_song(self):
        """垃圾桶"""
        self.current_playlist = self._get_playlist(params={'type':'b','sid': self.current_song.get('sid')})
        self.current_cur = -1

    def heart_song(self):
        """红心"""
        current_song = self.current_song
        if int(current_song.get('like')) != 1:
            self.current_playlist.extend(self._get_playlist(params={'type':'r','sid': current_song.get('sid')}))
            self.current_song['like'] = 1

    def unheart_song(self):
        """红心"""
        current_song = self.current_song
        if int(current_song.get('like')) != 0:
            self.current_playlist.extend(self._get_playlist(params={'type':'u','sid': current_song.get('sid')}))
            self.current_song['like'] = 0

if __name__ == '__main__':
    print 'TODO'
