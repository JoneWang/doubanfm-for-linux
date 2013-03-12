# coding=utf-8

import urllib
import requests
import json
import pynotify
import sys
import time
import re
import os
import pygst
pygst.require('0.10')
import gst
from util import getch
from share import set_skype_status

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
COOKIE_PATH = os.path.join(ROOT_PATH, '.cookie')
cookie = None
if os.path.exists(COOKIE_PATH):
    with open(COOKIE_PATH) as fh:
        cookie = fh.read().strip()

channelurl = 'http://douban.fm/j/explore/hot_channels'

channelurl_list_params = {
            'start': '0',
            'limit': '10',
        }

fmurl= 'http://douban.fm/j/mine/playlist'

music_list_params = {
            'type': 'n',
            'channel': '32',
            'from': 'mainsite',
            'r': '720db0723e',
            'kbps':'192',
        }

def get_channel_list(page_num):
    limit = 20
    start = page_num*limit
    channelurl_list_params['start'] = start
    channelurl_list_params['limit'] = limit
    channel_list_data = _request_url(channelurl, channelurl_list_params)
    channel_list = json.loads(channel_list_data)['data']['channels']
    if channel_list == []:
        return False
    print ''.ljust(55, '-')
    print '|', 'Channel'.ljust(25, ' ') ,' ID '.ljust(12, ' '), 'Music Count'.ljust(12, ' '), '|'
    print ''.ljust(55, '-')
    for id in range(len(channel_list)):
        channel = channel_list[id]
        name = channel['name']
        song_num = str(channel['song_num'])
        name_zh = len_zh(name)
        print '|', ('%s MHz' % name).ljust(24-name_zh, ' '), (' [%s] ' % channel['id']).ljust(15, ' '), song_num.ljust(10, ' '), '|'
    print ''.ljust(55, '-')
    print '|', ('Current Page: %s' % (page_num+1)).ljust(51, ' '), '|'
    print ''.ljust(55, '-')
    return True

def get_music_list(channel_id, type='n'):
    music_list_params['channel'] = str(channel_id)
    music_list = _request_url(fmurl, music_list_params)
    data = json.loads(music_list)
    if data['r'] == 0:
        return json.loads(music_list)['song']
    else:
        return []

def played_music_log(music_info):
    log_path = ''.join([ROOT_PATH, '/musics.list'])
    text = ''
    if not os.path.exists(log_path):
        text += '[Play Time] Title | Album | Artist | Company\n'
    text += '[%s] %s | %s | %s | %s\n' % (
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            music_info.get('title', ''), 
            music_info.get('albumtitle', ''), 
            music_info.get('artist', ''), 
            music_info.get('company', ''))
    f = open((log_path), 'a')
    try:
        f.write(text)
    finally:
        f.close()


def _request_url(url, params):
    params_data = urllib.urlencode(params)
    url = '?'.join([url, params_data])
    headers = {}
    if cookie:
        headers['Cookie'] = cookie
    res = requests.get(url, headers ={'Cookie': cookie})
    return res.text


if not pynotify.init ("icon-summary"):
    sys.exit (1)

capabilities = {
        'actions':             False,
        'body':                False,
        'body-hyperlinks':     False,
        'body-images':         False,
        'body-markup':         False,
        'icon-multi':          False,
        'icon-static':         False,
        'sound':               False,
        'image/svg+xml':       False,
        'private-synchronous': False,
        'append':              False,
        'private-icon-only':   False
        }
 
def initCaps():
    caps = pynotify.get_server_caps()
    if caps is None:
        print "Failed to receive server caps."
        sys.exit(1)
 
    for cap in caps:
        capabilities[cap] = True

def len_zh(data):
    temp = re.findall('[^a-zA-Z0-9.\s]+', data)
    count = 0
    for i in temp:
        count += len(i)
    return(count)


def show_dialog(content, sub):
    n = pynotify.Notification(content, sub)
    n.show()

if __name__ == '__main__':

    page_start = 0
    channel_id = 0

    player = gst.element_factory_make("playbin", "player")
    initCaps()

    current_pos = 0
    for i in range(len(sys.argv)):
        if sys.argv[i] == 'c':
            channel_id = sys.argv[i+1]
    
    '''
    if channel_id == 0:
        get_channel_list(page_start)
        while True:
            print 'Enter ID select channel.'
            print 'Enter "n" turn to next page or "p" turn to previous page.'
            cmd = '1'#raw_input('Command:') TODO bug here
            if cmd.isdigit():
                channel_id = int(cmd)
                music_list = get_music_list(channel_id)
                if music_list == []:
                    print '[info] Not found channel.\n'
                else:
                    break
            else:
                if cmd == 'n':
                    page_start += 1
                    if not get_channel_list(page_start):
                        print '[info] List is already last page.\n'
                elif cmd == 'p':
                    if page_start != 0:
                        page_start -= 1
                        get_channel_list(page_start)
                    else:
                        print '[info] List is already first page.\n'
    '''
    channel_id = 0
    print 'Channel: %s' % channel_id
    music_list = get_music_list(channel_id)

    bus = player.get_bus()
    bus.add_signal_watch()

    music_list = get_music_list(channel_id)
        
    def play_song(pos=0):
        item = music_list[pos]
        show_dialog(item['albumtitle'], item['artist'])
        if item == music_list[-1]:
            music_list.extend(get_music_list(channel_id))
        print ''
        print 'Music Info'
        print '==============='
        print 'Name: %s' % item.get('title')
        print 'Album: %s' % item.get('albumtitle')
        print 'Artist: %s' % item.get('artist')
        print 'Company: %s' % item.get('company')
        print '==============='
        played_music_log(item)
        player.set_property('uri',item['url'])
        player.set_state(gst.STATE_PLAYING)
        set_skype_status('♪ 正在豆瓣FM上收听: %s - %s' % (item.get('artist'), item.get('title')))
        

    def on_message(bus, message):
        global current_pos
        t = message.type
        if t == gst.MESSAGE_EOS:
            player.set_state(gst.STATE_NULL)
            current_pos += 1
            play_song(current_pos)
        elif t == gst.MESSAGE_ERROR:
            player.set_state(gst.STATE_NULL)
            current_pos += 1
            play_song(current_pos)
    bus.connect("message", on_message)
    
    play_song(0)
    
    while True:
        c = getch()
        if c == 'n':
            player.set_state(gst.STATE_NULL)
            music_list = get_music_list(channel_id, type='s') #skip
            current_pos = 0
            play_song(current_pos)
        elif c == 'p':
            player.set_state(gst.STATE_NULL)
        elif c == 'P':
            player.set_state(gst.STATE_PLAYING)
        elif c == 'Q':
            player.set_state(gst.STATE_NULL)
            break
        elif c == 'r':
            music_list.extend(get_music_list(channel_id,type='r'))
            print '❤\'ed %s' % music_list[current_pos].get('title') 

        #TODO red ...

