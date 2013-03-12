# coding: UTF-8
import Skype4Py

# Create an instance of the Skype class.
skype = Skype4Py.Skype()

# Connect the Skype object to the Skype client.
skype.Attach()

def set_skype_status(msg):
    skype.CurrentUserProfile.MoodText = msg
