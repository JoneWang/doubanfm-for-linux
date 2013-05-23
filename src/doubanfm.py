# coding=utf-8

import urllib
import json
import gst
import gtk
import appindicator
import webbrowser
import os

__version__ = '0.4.1'
__author__ = 'Jone Wang (i.jonewang@gmail.com)'

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

user_session = {}

class DoubanAPI(object):

    def __init__(self):
        self.channelurl = 'http://douban.fm/j/explore/hot_channels'
        self.channelurl_list_params = {
                    'start': '0',
                    'limit': '10',
                }
        self.fmurl= 'http://douban.fm/j/mine/playlist'
        self.music_list_params = {
                    'type': 'n',
                    'channel': '32',
                    'from': 'mainsite',
                    'r': '73072e1c06',
                }
        self.verification_url = 'http://douban.fm/j/new_captcha'
        self.verification_image_url = 'http://douban.fm/misc/captcha'
        self.login_url = 'http://douban.fm/j/login'

    def get_music_list(self, channel_id):
        self.music_list_params['channel'] = str(channel_id)
        music_list = self._request_url(self.fmurl, self.music_list_params).read()
        data = json.loads(music_list)
        if data['r'] == 0:
            return json.loads(music_list)['song']
        else:
            return []

    def get_verification_code(self):
        self.code = self._request_url(self.verification_url).read()[1:-1]
        image = self._request_url(self.verification_image_url, {'size': 'm', 'id': self.code}).read()
        return image

    def get_session(self, email, password, verification_code):
        resp = self._request_url(self.login_url, {
            'source': 'radio',
            'alias': email,
            'form_password': password,
            'captcha_solution': verification_code,
            'captcha_id': self.code,
            'task': 'sync_channel_list',
        })
        print resp.headers.get('Set-Cookie', '')

    def _request_url(self, url, params={}):
        params_data = urllib.urlencode(params)
        if params_data: url = '?'.join([url, params_data])
        data = urllib.urlopen(url)
        return data


class Player():

    def __init__(self):
        self.player = gst.element_factory_make("playbin2", "player")
        fakesink = gst.element_factory_make("fakesink", "fakesink")
        self.player.set_property("video-sink", fakesink)
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        #bus.connect("sync-message::element", self.on_sync_message)

    def start(self, uri):
        self.player.set_state(gst.STATE_NULL)
        self.player.set_property("uri", uri)
        self.player.set_state(gst.STATE_PLAYING)

    def stop(self):
        self.player.set_state(gst.STATE_NULL)

    def conti(self):
        self.player.set_state(gst.STATE_PLAYING)

    def pause(self):
        self.player.set_state(gst.STATE_PAUSED)

    def connect(self, event, func):
        if event == 'play_end':
            self.on_play_end = func

    def on_play_end():
        pass

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.on_play_end()
    

class EventUnrealizedException(Exception):
    def __init__(self, event_name):
        Exception.__init__(self)
        self.value = event_name

    def __str__(self):
        return repr('Event %s is Unrealized.' % self.value)


class TrayLayout(object):

    def __init__(self):
        menus_data = [
            {'icon': 'pause.png', 
             'id': 'menu_start_stop', 'name': 'Pause', 'event': self.event_start_pause_music}, 
            {'icon': 'next.png', 
             'id': 'menu_next', 'name': 'Next', 'event': self.event_next_music}, 
            {'icon': 'like.png', 
             'id': 'menu_like', 'name': 'Like', 'event': self.event_like_music}, 
            {'icon': 'info.png', 
             'id': 'menu_info', 'name': 'Music Info', 'event': self.event_info_music}, 
            {'icon': 'user.png', 
             'id': 'menu_login', 'name': 'Login', 'event': self.event_login},
            {'icon': 'channel.png', 
             'id': 'menu_login', 'name': 'Channel', 'event': self.event_login},
            {'icon': 'about.png', 
             'id': 'menu_login', 'name': 'About', 'event': self.event_login},
            {'icon': 'exit.png', 
             'id': 'menu_quit', 'name': 'Exit', 'event': gtk.main_quit}
        ]
        menu = self._init_menu(menus_data)
        self._init_tray_icon(menu)

    def _init_tray_icon(self, menu):
        self.ind = appindicator.Indicator('example-simple-client',
                                      os.path.join(ROOT_PATH, 'icons', 'music.png'),
                                      appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_menu(menu)

    def _init_menu(self, menus_data):
        menu = gtk.Menu()
        for menu_data in menus_data:
            menu_item = gtk.ImageMenuItem()
            menu_item.set_label(menu_data['name'])
            setattr(TrayLayout, menu_data['id'], menu_item)

            menu_item.set_use_stock(True)
            menu_item.set_always_show_image(True)

            self._set_menu_icon(menu_item, menu_data['icon'])
            menu_item.connect('activate', menu_data['event'])
            menu.append(menu_item)
            menu_item.show()
        return menu

    def _set_tray_icon(self, icon):
        self.ind.set_icon(os.path.join(ROOT_PATH, 'icons', icon))
        self.ind.set_attention_icon(os.path.join(ROOT_PATH, 'icons', icon))

    def _set_menu_icon(self, menu, icon):
        img = gtk.Image()
        img.set_from_file(os.path.join(ROOT_PATH, 'icons', icon))
        img.show()
        menu.set_image(img)

    def event_start_pause_music(self, argv):
        if self.menu_start_stop.get_label() == 'Continue' or not argv:
            self.continue_music(argv)
            self.menu_start_stop.set_label('Pause')
            self._set_menu_icon(self.menu_start_stop, 'pause.png')
            self._set_tray_icon('music.png')
        else:
            self.pause_music(argv)
            self.menu_start_stop.set_label('Continue')
            self._set_menu_icon(self.menu_start_stop, 'play.png')
            self._set_tray_icon('music_stop.png')

    def event_start_music(self, argv):
        pass

    def event_login(self, argv):
        LoginWdindow()

    def set_tray_title(self, title):
        self.ind.set_label(title)

    def event_next_music(self, argv):
        self.next_music(argv)
        self.menu_start_stop.set_label('Pause')

    def event_like_music(self, argv):
        pass

    def event_info_music(self, argv):
        uri = self.info_music()
        webbrowser.open(uri)

    def start_music(self, argv):
        raise EventUnrealizedException('start_music')

    def pause_music(self, argv):
        raise EventUnrealizedException('start_music')

    def continue_music(self, argv):
        raise EventUnrealizedException('continue_music')

    def stop_music(self, argv):
        #raise EventUnrealizedException('stop_music')
        pass

    def next_music(self, argv):
        raise EventUnrealizedException('next_music')

    def info_music(self, argv):
        raise EventUnrealizedException('info_music')



session = None

class TrayMenu(TrayLayout):

    def __init__(self):
        super(TrayMenu, self).__init__()
        self.is_pause = False
        self.player = Player()
        self.player.connect('play_end', self.next_music)
        self.douban = DoubanAPI()
        self.new_list()
        self.start_music()

    def new_list(self):
        self.current = 0
        self.music_list = self.douban.get_music_list('28')

    def start_music(self, argv=None):
        music_info = self.music_list[self.current]
        if music_info==self.music_list[-1] or self.is_pause:
            self.new_list()
            self.is_pause = False
        self.player.start(music_info['url'])
        self.set_tray_title(music_info['title'])

    def continue_music(self, argv=None):
        self.player.conti()

    def stop_music(self, argv=None):
        self.player.stop()

    def pause_music(self, argv=None):
        self.player.pause()
        self.is_pause = True

    def next_music(self, argv=None):
        self.current += 1
        self.start_music()

    def info_music(self, argv=None):
        return 'http://music.douban.com/%s' % self.music_list[self.current]['album']

    def show_login(self, argv=None):
        LoginWdindow()


class LoginWdindow(gtk.Window):
    
    def __init__(self):
        self.douban = DoubanAPI()

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Login')
        window.set_default_size(400, -1)
        #window.connect('EXPOSE', self.expose)
        vbox = gtk.VBox()
        window.add(vbox)

        self.entry_email = gtk.Entry()
        vbox.pack_start(self.entry_email, False, True)
        self.entry_password = gtk.Entry()
        self.entry_password.set_visibility(False)
        self.entry_password.set_invisible_char('*')
        vbox.pack_start(self.entry_password, False, True)
        self.entry_code = gtk.Entry()
        vbox.pack_start(self.entry_code, False, True)

        self.image_ver = gtk.Image()
        #self.image_ver.set_from_pixbuf(pixbuf)
        self.image_ver.show()
        vbox.add(self.image_ver)

        self.button = gtk.Button('Login')
        self.button.connect("clicked", self.login)
        vbox.add(self.button)
        window.show_all()

    def expose(self, argv):
        ver_data = self.douban.get_verification_code()
        loader = gtk.gdk.PixbufLoader()
        loader.write(ver_data, len(ver_data))
        pixbuf = loader.get_pixbuf()
        self.image_ver.set_from_pixbuf(pixbuf)

    def login(self, argv):
        self.douban.get_session(
                self.entry_email.get_text(), 
                self.entry_password.get_text(), 
                self.entry_code.get_text()
            )
        
if __name__ == '__main__':
    TrayMenu()
    gtk.main()

