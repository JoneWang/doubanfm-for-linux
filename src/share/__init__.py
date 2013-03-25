# coding: UTF-8
import warnings

def set_skype_status(msg):
    pass

def notify(*argv):
    pass

try:
    import Skype4Py
    # Create an instance of the Skype class.
    skype = Skype4Py.Skype()
    # Connect the Skype object to the Skype client.
    skype.Attach()
    def set_skype_status(msg):
        skype.CurrentUserProfile.MoodText = msg
except Exception, e:
    pass

try:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        import pynotify
        pynotify.init ("icon-summary")
        if len(w) == 0:
            def notify(i_artist, i_title, i_cover_path):
                n = pynotify.Notification(i_artist, i_title, i_cover_path)
                n.show()
except:
    pass
