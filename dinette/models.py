from django.db import models
from django.contrib.auth.models import User,Group
from django.conf import settings
from django.contrib.sites.models import Site
from django import forms
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.template.defaultfilters import truncatewords

import logging
import logging.config
from datetime import datetime
import hashlib
from BeautifulSoup import BeautifulSoup
import datetime
from dinette.libs.postmarkup import render_bbcode
from markupfield.fields import MarkupField

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
        verbose_name = "Super Category"
        verbose_name_plural = "Super Categories"
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
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ('ordering','-created_on' )    
    
    
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
        for topic in self.get_topics():
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
        return self.lastPost().posted_by
        
     
    def lastPost(self):
        if(self.ftopics_set.count() == 0):
            return self   
        obj = self.ftopics_set.order_by('-created_on')[0]        
        if (obj.reply_set.count() > 0 ):
            return obj.reply_set.order_by("-created_on")[0]
        else :
            return obj  
    
    def get_topics(self):
        return Ftopics.objects.filter(category=self)

    def __unicode__(self):
        return self.name 
    
class TopicManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        return super(TopicManager, self).get_query_set().filter(is_hidden = False)
    
    def get_new_since(self, when):
        "Topics with new replies after @when"
        now = datetime.datetime.now()
        return self.filter(last_reply_on__gt = now)
    

class Ftopics(models.Model):
    category = models.ForeignKey(Category)
    posted_by = models.ForeignKey(User)
    
    subject = models.CharField(max_length=999)
    slug = models.SlugField(max_length = 200, db_index = True) 
    message = MarkupField(default_markup_type=getattr(settings,
                                                      'DEFAULT_MARKUP_TYPE',
                                                      'markdown'),
                          markup_choices=settings.MARKUP_RENDERERS,
                          escape_html=True,
                          )
    file = models.FileField(upload_to='dinette/files',default='',null=True,blank=True)
    attachment_type = models.CharField(max_length=20,default='nofile')
    filename = models.CharField(max_length=100,default="dummyname.txt")
    viewcount = models.IntegerField(default=0)
    replies = models.IntegerField(default=0)    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    last_reply_on = models.DateTimeField(auto_now_add=True)
    num_replies = models.PositiveSmallIntegerField(default = 0)
    
    #Moderation features
    announcement_flag = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    is_sticky = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    
    # use TopicManager as default, prevent leaking of hidden topics
    default = models.Manager()
    objects = TopicManager()

    # for topic subscriptions
    subscribers = models.ManyToManyField(User, related_name='subscribers')
    
    class Meta:
        ordering = ('-is_sticky', '-last_reply_on',)
        get_latest_by = ('created_on')
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
        
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.subject)
            slug = slug[:198]
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
        
    def search_snippet(self):
        msg = "%s %s"% (self.subject, self.message.rendered)
        return truncatewords(msg, 50) 
        
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
         

class ReplyManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        return super(ReplyManager, self).get_query_set().filter(topic__is_hidden=False)

# Create Replies for a topic
class Reply(models.Model):
    topic = models.ForeignKey(Ftopics)
    posted_by = models.ForeignKey(User)

    message = MarkupField(default_markup_type=getattr(settings,
                                                      'DEFAULT_MARKUP_TYPE',
                                                      'markdown'),
                          markup_choices=settings.MARKUP_RENDERERS,
                          escape_html=True,
                          )
    file = models.FileField(upload_to='dinette/files',default='',null=True,blank=True)
    attachment_type = models.CharField(max_length=20,default='nofile')
    filename = models.CharField(max_length=100,default="dummyname.txt")
    
    reply_number = models.SmallIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    # replies for hidden topics should be hidden as well
    default = models.Manager()
    objects = ReplyManager()

    class Meta:
        verbose_name = "Reply"
        verbose_name_plural = "Replies"
        ordering = ('created_on',)
        get_latest_by = ('created_on', )
        
    def save(self, *args, **kwargs):
        if not self.pk:
            self.reply_number = self.topic.reply_set.all().count() + 1
        super(Reply, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return truncatewords(self.message, 10)
    
    def search_snippet(self):
        msg = "%s %s"%(self.message.rendered, self.topic.subject)
        return truncatewords(msg, 100)
    
    
    @models.permalink
    def get_absolute_url(self):
        return ('dinette_topic_detail',(),{'categoryslug':self.topic.category.slug,'topic_slug': self.topic.slug})
    
    def get_url_with_fragment(self):
        page = (self.reply_number-1)/settings.REPLY_PAGE_SIZE + 1
        url =  self.get_absolute_url()
        if not page == 1:
            return "%s?page=%s#%s" % (url, page, self.reply_number)
        else:
            return "%s#%s" % (url, self.reply_number)
            
    
    def htmlfrombbcode(self):
        soup = BeautifulSoup(self.message.raw)
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
    user = models.ForeignKey(User, unique = True)
    last_activity = models.DateTimeField(auto_now_add=True)
    #When was the last session. Used in page activity since last session.
    last_session_activity = models.DateTimeField(auto_now_add=True)
    userrank = models.CharField(max_length=30,default="Junior Member")
    last_posttime = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='dinette/files',null=True,blank=True)
    signature = models.CharField(max_length = 1000, null = True, blank = True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    is_subscribed_to_digest = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.user.username
    
    #Populate the user fields for easy access
    @property
    def username(self):
        return self.user.username
    
    @property
    def first_name(self):
        return self.user.first_name
    
    @property
    def last_name(self):
        return self.user.last_name
    
    
    def get_total_posts(self):
        print self.user.ftopics_set.count() + self.user.reply_set.count()
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
    
    def get_since_last_visit(self):
        "Topics with new relies since last visit"
        return Ftopics.objects.get_new_since(self.last_session_activity)
     
    @models.permalink
    def get_absolute_url(self):
        return ('dinette_user_profile', [self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.user.username)
            if slug:
                same_slug_count = self._default_manager.filter(slug__startswith=slug).count()
                if same_slug_count:
                    slug = slug + str(same_slug_count)
                self.slug = slug
            else:
                #fallback to user id
                slug = self.user.id
        super(DinetteUserProfile, self).save(*args, **kwargs)
    
class NavLink(models.Model):
    title = models.CharField(max_length = 100)
    url = models.URLField()
    
    class Meta:
        verbose_name = "Navigation Link"
        verbose_name_plural = "Navigation Links"
        
    def __unicode__(self):
        return self.title
    
       
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        DinetteUserProfile.objects.create(user=instance)
        
def update_topic_on_reply(sender, instance, created, **kwargs):
    if created:
        instance.topic.last_reply_on = instance.created_on
        instance.topic.num_replies += 1
        instance.topic.save()

def notify_subscribers_on_reply(sender, instance, created, **kwargs):
    if created:
        site = Site.objects.get_current()
        subject = "%s replied on %s" %(instance.posted_by, instance.topic.subject)
        body = instance.message.rendered
        from_email = getattr(settings, 'DINETTE_FROM_EMAIL', '%s notifications <admin@%s>' %(site.name, site.domain))
        # exclude the user who posted this, even if he is subscribed
        for subscriber in instance.topic.subscribers.exclude(username=instance.posted_by.username):
            subscriber.email_user(subject, body, from_email)

post_save.connect(create_user_profile, sender=User)
post_save.connect(update_topic_on_reply, sender=Reply)
post_save.connect(notify_subscribers_on_reply, sender=Reply)

