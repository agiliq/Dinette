from django.conf.urls.defaults import *
from django.contrib.syndication.views import feed

from dinette.views import LatestTopicsByCategory,LatestRepliesOfTopic

feeds = {
   'category': LatestTopicsByCategory,
   'topic': LatestRepliesOfTopic
}



urlpatterns = patterns('dinette.views',
    url(r'^$','indexPage',name='dinette_category'),                       
    url(r'^category/(?P<categoryslug>[\w-]+)/topics/$','welcomePage', name='dinette_index'),
    url(r'^category/(?P<categoryslug>[\w-]+)/topics/page(?P<pageno>\d+)/$','welcomePage', name='dinette_index2'),
    url(r'^post/topic/$','postTopic', name='dinette_posttopic'),
    url(r'^post/reply/$','postReply', name='dinette_postreply'),
    url(r'^topics/list/$','topic_list', name='dinette_topic_list'),
    url(r'^topics/detail/(?P<topic_id>\d+)/$','topic_detail', name='dinette_topic_detail'),
    url(r'^topics/detail/(?P<topic_id>\d+)/page(?P<pageno>\d+)/$','topic_detail', name='dinette_reply_detail'),
    
    )

urlpatterns += patterns('',
                    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed' , {'feed_dict': feeds},name='dinette_feed_url') ,
                    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed' , {'feed_dict': feeds},name='dinette_topic_url') 
                    
                        )
