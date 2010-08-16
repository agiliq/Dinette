from django.conf.urls.defaults import *
from django.contrib.syndication.views import feed

from dinette.views import LatestTopicsByCategory,LatestRepliesOfTopic

feeds = {
   'category': LatestTopicsByCategory,
   'topic': LatestRepliesOfTopic
}



urlpatterns = patterns('dinette.views',
    url(r'^$','index_page',name='dinette_category'),
    url(r'^new/$','new_topics',name='dinette_new_for_user'),                         
    url(r'^active/$','active',name='dinette_active'),
    url(r'^unasnwered/$','active',name='dinette_unanswered'),
    #Login page, needs to be before category_details, or gets caught by that regex.
    url(r'^login/$','login',name='dinette_login'),    
    
    url(r'^search/$','search',name='dinette_search'),
    
    # user profile page
    url(r'^users/(?P<slug>[\w-]+)$', 'user_profile', name='dinette_user_profile'),

    # subscribe to digest
    url(r'^digest/subscribe/$', 'subscribeDigest', name='dinette_subscribe_to_digest'),
    url(r'^digest/unsubscribe/$', 'unsubscribeDigest', name='dinette_unsubscribe_from_digest'),
    
    url(r'^(?P<categoryslug>[\w-]+)/$','category_details', name='dinette_index'),
    url(r'^(?P<categoryslug>[\w-]+)/page(?P<pageno>\d+)/$','category_details', name='dinette_index2'),
    url(r'^post/topic/$','postTopic', name='dinette_posttopic'),
    url(r'^post/reply/$','postReply', name='dinette_postreply'),
    url(r'^(?P<categoryslug>[\w-]+)/(?P<topic_slug>[\w-]+)/$','topic_detail', name='dinette_topic_detail'),
    url(r'^(?P<categoryslug>[\w-]+)/(?P<topic_slug>[\w-]+)/page(?P<pageno>\d+)/$','topic_detail', name='dinette_reply_detail_paged'),
    
    #moderation views - Hence dont bother with SEF urls
    url(r'^moderate/topic/(?P<topic_id>\d+)/close/$','moderate_topic', {'action':'close'}, name='dinette_moderate_close'),
    url(r'^moderate/topic/(?P<topic_id>\d+)/stickyfy/$','moderate_topic', {'action':'sticky'}, name='dinette_moderate_sticky'),
    url(r'^moderate/topic/(?P<topic_id>\d+)/annoucement/$','moderate_topic', {'action':'announce'}, name='dinette_moderate_announce'),
    url(r'^moderate/topic/(?P<topic_id>\d+)/hide/$','moderate_topic', {'action':'hide'}, name='dinette_moderate_hide'),
    
    # post actions, permitted to OP and mods
    url(r'^delete/reply/(?P<reply_id>\d+)$','deleteReply', name='dinette_deletereply'),
    url(r'^edit/reply/(?P<reply_id>\d+)$','editReply', name='dinette_editreply'),

    # subscribe to topic
    url(r'^subscribe/topic/(?P<topic_id>\d+)', 'subscribeTopic', name='dinette_subscribe_to_topic'),
    url(r'^unsubscribe/topic/(?P<topic_id>\d+)', 'unsubscribeTopic', name='dinette_unsubscribe_from_topic'),
)


urlpatterns += patterns('',
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed' , {'feed_dict': feeds},name='dinette_feed_url'),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed' , {'feed_dict': feeds},name='dinette_topic_url'),
)
