from django.http import HttpResponse

import datetime

from dinette.models import DinetteUserProfile

class UserActivity:
    def process_request(self, req):
        if req.user.is_authenticated():
            #last = req.user.get_profile().last_activity
            user_profile = req.user.get_profile()
            now = datetime.datetime.now()
            user_profile.last_activity=now
            user_profile.save()