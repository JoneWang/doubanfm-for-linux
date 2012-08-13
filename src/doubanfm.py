import urllib
import json
import pynotify
import sys
import time
import mdecode

fmurl= 'http://douban.fm/j/mine/playlist?'

music_list_params = {
            'type': 'n',
            'channel': '32',
            'from': 'mainsite',
        }

def get_music_list():
    params_data = urllib.urlencode(music_list_params)
    print params_data
    data = urllib.urlopen(''.join([fmurl, params_data]))
    music_list = data.read()
    print music_list
    return json.loads(music_list)['song']


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


def show_dialog(content, sub):
    n = pynotify.Notification(content, sub)
    n.show()


if __name__ == '__main__':
    mdecode.initVM(classpath=mdecode.CLASSPATH)
    initCaps()

    music_list = get_music_list()
    for item in music_list:
        show_dialog(item['albumtitle'], item['artist'])
        if item == music_list[-1]:
            music_list.extend(get_music_list())
        mdecode.Play.main([item['url']])
        
