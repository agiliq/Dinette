Dinette - A Django based forum inspired by PhpBB
-----------------------------------------------------------


Requirements
------------------------------

Dinette requires the following to be installed.

1. Python 2.5+ (May work with lower, but hasn't been tested.)
2. Django 1.1+ (May work with 1.0, but hasn't been tested.)
3. The following Django apps are used in templates, so if you use the default templates, you need them as well.

3.1 django-pagination
3.2 sorl-thumbnail
3.3 django-compressor

4. If you need to migrate between install, south.

Install instructions
------------------------------
1. Add `dinette` to your INSTALLED_APPS
2. `syncdb` and/or `migrate`
3. Add following settings with values for your install.

#topic page size
TOPIC_PAGE_SIZE = 10 # Number of topics one a page to paginate by
#REPLY PAGE SIZE 
REPLY_PAGE_SIZE = 10 # Number of replies one a page to paginate by
#Flood Time
FLOOD_TIME = 5 #Time in seconds between consecutive posts by a user. 
#internal ip
AUTH_PROFILE_MODULE = 'dinette.DinetteUserProfile' # For use by user.get_profile()
RANKS_NAMES_DATA = ((30, "Member"), (100, "Senior Member"), (300, 'Star'))
DINETTE_LOGIN_TEMPLATE = 'dinette/social_login.html'

#settings used by socialauth

#Get them from facebook and twitter. Read socialauth documentation for more info
TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''

FACEBOOK_API_KEY = ''
FACEBOOK_API_SECRET = ''


OPENID_REDIRECT_NEXT = '/accounts/openid/done/'
OPENID_SREG = {"requred": "nickname, email", "optional":"postcode, country", "policy_url": ""}
OPENID_AX = [{"type_uri": "email", "count": 1, "required": False, "alias": "email"}, {"type_uri": "fullname", "count":1 , "required": False, "alias": "fullname"}]
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',
                           'socialauth.auth_backends.OpenIdBackend',
                           'socialauth.auth_backends.TwitterBackend',
                           'socialauth.auth_backends.FacebookBackend',
                           )
LOGIN_REDIRECT_URL = '/login/done/'                           
SITE_NAME = 'uswaretech.com'#This is used by socialauth.

4. Add the following to your context processors.

"dinette.context_processors.get_announcement"
"dinette.context_processors.get_site_config"

5. If you are using django-pagination, 

  * add "django.core.context_processors.request" to your context processors

  * add "pagination.middleware.PaginationMiddleware" to your middleware 

6. Via admin add to `SuperCategory` and `Category`. Add moderators to `Category` who get some extra powers!

7. ???

8. Profit.

 


