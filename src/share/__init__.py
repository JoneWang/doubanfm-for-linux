# coding: UTF-8

try:
    import Skype4Py
    # Create an instance of the Skype class.
    skype = Skype4Py.Skype()
    # Connect the Skype object to the Skype client.
    skype.Attach()
    def set_skype_status(msg):
        skype.CurrentUserProfile.MoodText = msg
except Skype4Py.errors.SkypeAPIError, e:
    print 'warning:', e
    def set_skype_status(msg):
        pass


