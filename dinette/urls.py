from django.conf.urls.defaults import *
from django.contrib.syndication.views import feed

from dinette.views import LatestTopicsByCategory,LatestRepliesOfTopic

feeds = {
   'category': LatestTopicsByCategory,
   'topic': LatestRepliesOfTopic
}



urlpatterns = patterns('dinette.views',
    url(r'^$','indexPage',name='djorum_category'),                       
    url(r'^category(?P<categoryid>\d+)/topics/$','welcomePage', name='djorum_index'),
    url(r'^category(?P<categoryid>\d+)/topics/page(?P<pageno>\d+)/$','welcomePage', name='djorum_index2'),
    url(r'^post/topic/$','postTopic', name='djorum_posttopic'),
    url(r'^post/reply/$','postReply', name='djorum_postreply'),
    url(r'^topics/list/$','topic_list', name='djorum_topic_list'),
    url(r'^topics/detail/(?P<topic_id>\d+)/$','topic_detail', name='djorum_topic_detail'),
    url(r'^topics/detail/(?P<topic_id>\d+)/page(?P<pageno>\d+)/$','topic_detail', name='djorum_reply_detail'),
    
    )

urlpatterns += patterns('',
                    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed' , {'feed_dict': feeds},name='djorum_feed_url') ,
                    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed' , {'feed_dict': feeds},name='djorum_topic_url') 
                    
                        )
