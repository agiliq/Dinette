from django.db import models
from django.contrib.auth.models import User,Group
from django.conf import settings
from django import forms
from django.template.defaultfilters import slugify

import logging
import logging.config
from datetime import datetime
import hashlib
from BeautifulSoup import BeautifulSoup
import datetime
from dinette.libs.postmarkup import render_bbcode

#loading the logging configuration
logging.config.fileConfig(settings.LOG_FILE_NAME,defaults=dict(log_path=settings.LOG_FILE_PATH))
 
#Create module logger 
mlog=logging.getLogger(__name__) 
mlog.debug("From settings LOG_FILE_NAME %s LOG_FILE_PATH %s" % (settings.LOG_FILE_NAME,settings.LOG_FILE_PATH))
mlog.debug("Models Compliing!"+__name__)

class SiteConfig(models.Model):
    name = models.CharField(max_length = 100)
    tag_line = models.TextField(max_length = 100)

class SuperCategory(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField(default='')
    ordering = models.PositiveIntegerField(default = 1)    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User)   
    accessgroups  = models.ManyToManyField(Group,related_name='can_access_forums')
    
    class Meta:
        ordering = ('-ordering', 'created_on')
        
    def __unicode__(self):
        return self.name
 
    
class Category(models.Model):
    name = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 110)
    description = models.TextField(default='')
    ordering = models.PositiveIntegerField(default = 1)
    super_category = models.ForeignKey(SuperCategory)    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, related_name='cposted')
    moderated_by = models.ManyToManyField(User, related_name='moderaters')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            same_slug_count = Category.objects.filter(slug__startswith = slug).count()
            if same_slug_count:
                slug = slug + str(same_slug_count)
            self.slug = slug
        super(Category, self).save(*args, **kwargs)
    
    @models.permalink
    def get_absolute_url(self):
        #return ('welcomePage', [self.slug])
        return ('dinette_index',(),{'categoryslug':self.slug})
    
    def getCategoryString(self):
        return "category/%s" % self.slug
    
    
    def noofPosts(self):
        count = 0
        for topic in self.ftopics_set.all() :
              #total posts for this topic = total replies + 1 (1 is for the topic as we are considering it as topic)
              count += topic.reply_set.count() + 1
        mlog.debug("TOtal count =%d " % count)
        return count
    
    
    def lastPostDatetime(self):
        ''' we are assuming post can be topic / reply
         we are finding out the last post / (if exists) last reply datetime '''                
        return self.lastPost().created_on
        
        
        
        
    def lastPostedUser(self):
        '''  we are assuming post can be topic / reply
             we are finding out the last post / (if exists) last reply datetime '''
        return self.lastPost().posted_by.username
        
     
    def lastPost(self):
        if(self.ftopics_set.count() == 0):
            return self   
        obj = self.ftopics_set.order_by('-created_on')[0]        
        if (obj.reply_set.count() > 0 ):
            return obj.reply_set.order_by("-created_on")[0]
        else :
            return obj
        
    
    
    class Meta:
        ordering = ('ordering','-created_on' )    
    
    def __unicode__(self):
        return self.name 

class Ftopics(models.Model):
    category = models.ForeignKey(Category)
    subject = models.CharField(max_length=1024)
    slug = models.SlugField(max_length = 1034) 
    message = models.TextField()
    file = models.FileField(upload_to='dinette/files',default='',null=True,blank=True)
    attachment_type = models.CharField(max_length=20,default='nofile')
    filename = models.CharField(max_length=100,default="dummyname.txt")
    viewcount = models.IntegerField(default=0)
    replies = models.IntegerField(default=0)    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User)
    #Moderation features
    announcement_flag = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    is_sticky = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    
    
    class Meta:
        ordering = ('-is_sticky', '-updated_on',)
        get_latest_by = ('created_on')
        
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.subject)
            same_slug_count = Ftopics.objects.filter(slug__startswith = slug).count()
            if same_slug_count:
                slug = slug + str(same_slug_count)
            self.slug = slug
        super(Ftopics, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.subject
    
    @models.permalink
    def get_absolute_url(self):
        return ('dinette_topic_detail',(),{'categoryslug':self.category.slug, 'topic_slug': self.slug})
    
    
    def htmlfrombbcode(self):
        if(len(self.message.strip()) >  0):            
            return render_bbcode(self.message)
        else :
            return ""
        
    def getTopicString(self):
        #which is helpful for doing reverse lookup of an feed url for a topic         
        return "topic/%s" % self.slug
        
    def lastPostDatetime(self):
        return self.lastPost().created_on
        
        
        
        
    def lastPostedUser(self):
        return self.lastPost().posted_by.username
        
    
    
    def lastPost(self):
        if (self.reply_set.count() == 0):
            return self       
        return self.reply_set.order_by('-created_on')[0]        
        
        
    def classname(self):
         return  self.__class__.__name__
         

# Create Replies for a topic
class Reply(models.Model):
    message = models.TextField()
    file = models.FileField(upload_to='dinette/files',default='',null=True,blank=True)
    attachment_type = models.CharField(max_length=20,default='nofile')
    filename = models.CharField(max_length=100,default="dummyname.txt")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(Ftopics)
    posted_by = models.ForeignKey(User)
    
    class Meta:
        ordering = ('created_on',)
        get_latest_by = ('created_on', )
    
    def __unicode__(self):
        return self.message
    
    
    @models.permalink
    def get_absolute_url(self):
        return ('dinette_topic_detail',(),{'categoryslug':self.topic.category.slug,'topic_slug': self.topic.slug})
    
    def htmlfrombbcode(self):
        soup = BeautifulSoup(self.message)
        #remove all html tags from the message
        onlytext = ''.join(soup.findAll(text=True))
        
        #get the bbcode for the text
        if(len(onlytext.strip()) >  0):            
            return render_bbcode(onlytext)
        else :
            return ""
    
    def classname(self):
        return  self.__class__.__name__
        
        
class DinetteUserProfile(models.Model):
    user = models.ForeignKey(User)
    last_activity = models.DateTimeField(auto_now_add=True)
    userrank = models.CharField(max_length=30,default="Junior Memeber")
    last_posttime = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='dinette/files',null=True,blank=True)
    
    def get_total_posts(self):
        return self.user.ftopics_set.count() + self.user.reply_set.count()
    
    def is_online(self):
        from django.conf import settings
        last_online_duration = getattr(settings, 'LAST_ONLINE_DURATION', 900)
        now = datetime.datetime.now()
        if (now - self.last_activity).seconds < last_online_duration:
            return True
        return False   
    

    def getMD5(self):
        m = hashlib.md5()
        m.update(self.user.email)        
        return m.hexdigest()
    
    def get_absolute_url(self):
        return self.user.get_absolute_url()
       
 
        
     
      
    
     
