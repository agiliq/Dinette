from django.conf.urls.defaults import *
from django.contrib.syndication.views import feed

from dinette.views import LatestTopicsByCategory,LatestRepliesOfTopic

feeds = {
   'category': LatestTopicsByCategory,
   'topic': LatestRepliesOfTopic
}



urlpatterns = patterns('dinette.views',
    url(r'^$','indexPage',name='dinette_category'),                       
    url(r'^(?P<categoryslug>[\w-]+)/$','welcomePage', name='dinette_index'),
    url(r'^(?P<categoryslug>[\w-]+)/page(?P<pageno>\d+)/$','welcomePage', name='dinette_index2'),
    url(r'^post/topic/$','postTopic', name='dinette_posttopic'),
    url(r'^post/reply/$','postReply', name='dinette_postreply'),
    url(r'^topics/list/$','topic_list', name='dinette_topic_list'),
    url(r'^(?P<categoryslug>[\w-]+)/(?P<topic_slug>[\w-]+)/$','topic_detail', name='dinette_topic_detail'),
    url(r'^(?P<categoryslug>[\w-]+)/(?P<topic_slug>[\w-]+)/page(?P<pageno>\d+)/$','topic_detail', name='dinette_reply_detail'),
    
    )

urlpatterns += patterns('',
                    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed' , {'feed_dict': feeds},name='dinette_feed_url') ,
                    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed' , {'feed_dict': feeds},name='dinette_topic_url') 
                    
                        )
