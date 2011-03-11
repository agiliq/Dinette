from haystack import indexes
from haystack import site

from dinette.models import Ftopics, Reply, DinetteUserProfile

class TopicIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    subject = indexes.CharField(model_attr="subject")
    message = indexes.CharField(model_attr="_message_rendered")
    
class ReplyIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    message = indexes.CharField(model_attr="_message_rendered")
    
class UserprofileIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    username = indexes.CharField(model_attr="username")
    first_name = indexes.CharField(model_attr="first_name")
    last_name = indexes.CharField(model_attr="last_name")
    
site.register(Ftopics, TopicIndex)
site.register(Reply, ReplyIndex)
site.register(DinetteUserProfile, UserprofileIndex)
