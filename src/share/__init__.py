# coding: UTF-8
import warnings

def set_skype_status(*args, **kwargs):
    pass

def notify(*args, **kwargs):
    pass

try:
    import Skype4Py
    skype = Skype4Py.Skype()
    skype.Attach(Wait=False)
    def set_skype_status(msg):
        skype.CurrentUserProfile.MoodText = msg
except Exception, e:
    pass

try:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        import pynotify
        pynotify.init ("icon-summary")
        n = pynotify.Notification('Douban FM')
        n.show()
        if len(w) == 0:
            def notify(i_artist, i_title, i_cover_path):
                n = pynotify.Notification(i_artist, i_title, i_cover_path)
                n.show()
except:
    pass


def now_playing(song, channel_id, channel_name):
    t = u'♫ #NowPlaying# {artist} - {title} #{channel_name}# {song_url}'.format(\
            channel_name = channel_name
            , **song
            )
    set_skype_status(t)
