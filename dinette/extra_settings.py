# Dinette Settings
import os

TOPIC_PAGE_SIZE = 3

REPLY_PAGE_SIZE = 3

AUTH_PROFILE_MODULE = 'dinette.DinetteUserProfile'

RANKS_NAMES_DATA = ((30, "Member"), (100, "Senior Member"), (300, 'Star'))

FLOOD_TIME = 1000

HAYSTACK_SITECONF = "dinette.search"

HAYSTACK_SEARCH_ENGINE = 'whoosh'

HAYSTACK_WHOOSH_PATH = os.path.join(os.path.dirname(os.path.normpath(__file__)),'index.db')

SITE_URL = "http://127.0.0.1:8000"
