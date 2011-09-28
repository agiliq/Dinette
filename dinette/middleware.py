from django.http import HttpResponse

import datetime

from dinette.models import DinetteUserProfile

class UserActivity:
    def process_request(self, req):
        if req.user.is_authenticated():
            #last = req.user.get_profile().last_activity
            try:
                try:
                    user_profile = req.user.get_profile()
                except DinetteUserProfile.DoesNotExist:
                    now = datetime.datetime.now()
                    user_profile, created = DinetteUserProfile.objects.get_or_create(user = req.user, last_activity = now, last_session_activity = now)
                now = datetime.datetime.now()
                user_profile.last_activity=now
                dinette_activity_at = req.session.get("dinette_activity_at", [])
                req.session["dinette_activity_at"] = dinette_activity_at = rotate_with(dinette_activity_at, now)
                user_profile.last_session_activity = dinette_activity_at[0]
                user_profile.save()
            except:
                from django.conf import settings
                if settings.DEBUG:
                    raise
                else:
                    pass


                
def get_last_activity_with_hour_offset(lst, now = None):
    "Given a list of datetimes, find the most recent time which is at least one hour ago"
    if not now:
        now = datetime.datetime.now()
    from copy import deepcopy
    lst = deepcopy(lst)
    lst.reverse()
    for el in lst:
        if now - el > datetime.timedelta(hours =1):
            return el
    
            
def rotate_with(lst, el, maxsize = 10):
    """
    >>> rotate_with(range(5), 200)
    [200, 0, 1, 2, 3]
    >>> rotate_with(range(10), -1)
    [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8]
    >>> rotate_with([], 1)
    [1]
    >>> rotate_with([5, 2], -1)
    [-1, 5, 2]
    """
    if len(lst)>=maxsize:
        lst.pop()
    lst.insert(0, el)
    return lst
    
            

