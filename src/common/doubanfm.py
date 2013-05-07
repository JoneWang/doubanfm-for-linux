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
#from share import set_skype_status, notify
from plugin import test_filter
import BeautifulSoup

from common import logger as l

class DoubanFM(object):

    def __init__(self,start_url=None,debug=False):
        self._debug = debug
        self.ROOT_PATH = os.path.abspath(os.path.dirname(__file__) + '/../')
        self.COOKIE_PATH = os.path.join(self.ROOT_PATH, '.cookie')
        http_cookies = {}
        if os.path.exists(self.COOKIE_PATH):
            with open(self.COOKIE_PATH) as fh:
                cookies_text = fh.read().strip()
                try:
                    http_cookies = dict(cookie.split('=',1) for cookie in cookies_text.split('; '))
                except:
                    pass
        
        self.douban_fm_host = 'douban.fm'
        self.douban_fm_hot_channel_path = '/j/explore/hot_channels'
        self.douban_fm_playlist_path = '/j/mine/playlist'
        self.douban_fm_channel_detail_path = '/j/explore/channel_detail'
        self.douban_fm_channel_name= {0: u'私人兆赫', -3: u'红心兆赫'}
        self.douban_fm_default_params = {
                'type': 'n'
                , 'sid': ''
                , 'channel':0
                , 'pb': '192'
                , 'pt': 0.0
                , 'context':''
                , 'from':'mainsite'
                , 'kbps':'192'
                , 'r':'da01a52428'
                }
        
        self.http_session = requests.session()
        self.http_session.cookies.update(http_cookies)
        pre_request_url = start_url or ('http://%s/' % self.douban_fm_host)
        res = self.http_session.get(pre_request_url)
        try:
            soup = BeautifulSoup.BeautifulSoup(res.text)
            self.username = soup.find(id='user_name').text
        except:
            self.username = None
        if len(res.history) >= 1:
            last_visit = res.history[-1]
            if last_visit.status_code == 302:
                pre_request_url = last_visit.headers.get('location')

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

        self.channel_id = int(self.douban_fm_default_params['channel'])

        self.current_playlist = []
        self.current_cur = -1

        self.timeout = 3
        l.debug(u'username:{username}, channel:{channel}'.format(username=self.username, channel=self.channel_name))
        
    @property
    def current_song(self):
        if len(self.current_playlist) > 0:
            return self.current_playlist[self.current_cur]
        else:
            l.error('Ops...playlist is empty! exit')
            sys.exit()

    @property
    def channel_name(self):
        channel_name = self.douban_fm_channel_name.get(self.channel_id)
        if channel_name is not None:
            return channel_name

        params_data = 'channel_id=%d' % self.channel_id
        url = '?'.join(('http://%s%s' % (self.douban_fm_host, self.douban_fm_channel_detail_path), params_data))
        res = self.http_session.get(url)
        res_json = json.loads(res.text)
        if not res_json.get('status'):
            return None
        else:
            channel_name = res_json.get('data').get('channel').get('name')
            self.douban_fm_channel_name.update({self.channel_id: channel_name})
            return channel_name

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
            l.warning('cannot parse response json:\n {err}'.format(**res_json))
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
