# coding=utf-8

import urllib
import json
import pynotify
import sys
import time
import mdecode
import re
import os

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

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
            'r': '73072e1c06',
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

def get_music_list(channel_id):
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
    data = urllib.urlopen('?'.join([url, params_data]))
    return data.read()


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

    mdecode.initVM(classpath=mdecode.CLASSPATH)
    initCaps()

    for i in range(len(sys.argv)):
        if sys.argv[i] == 'c':
            channel_id = sys.argv[i+1]

    if channel_id == 0:
        get_channel_list(page_start)

        while True:
            print 'Enter ID select channel.'
            print 'Enter "n" turn to next page or "p" turn to previous page.'
            cmd = raw_input('Command:')
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




    music_list = get_music_list(channel_id)
    for item in music_list:
        show_dialog(item['albumtitle'], item['artist'])
        if item == music_list[-1]:
            music_list.extend(get_music_list(channel_id))
        print '\nMusic Info'
        print '==============='
        print 'Name:', item.get('title')
        print 'Album:', item.get('albumtitle')
        print 'Artist', item.get('artist')
        print 'Company', item.get('company')
        print '===============\n'
        played_music_log(item)
        mdecode.Play.main([item['url']])

