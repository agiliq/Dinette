from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.template import Context , loader
from django.template import RequestContext
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib.syndication.feeds import Feed
from django.contrib.auth.models import User , Group
from django.conf import settings
from django.views.generic.list_detail import object_list

from  datetime  import datetime
import logging
import simplejson

from dinette.models import Ftopics , SuperCategory ,Category ,Reply, DinetteUserProfile
from dinette.forms import  FtopicForm , ReplyForm



#Create module logger
#several logging configurations are configured in the models
mlogger = logging.getLogger(__name__)


def indexPage(request):
    mlogger.info("In the index page")
    forums = SuperCategory.objects.all()
    accesslist = ""
    jumpflag = False
    
    
    #groups which this user has access
    if request.user.is_authenticated() :
            groups = request.user.groups.all()
    else:
            #we are treating user who have not loggedin belongs to general group
            groups = Group.objects.filter(name="general")
        
    
    #logic which decide which forum does this user have access to
    for forum in forums :
        
        jumpflag = False
        for group in groups :           
            for gforum in group.can_access_forums.all() :
                
                if gforum.id == forum.id :
                    #the respective user can access the forum
                    #accesslist.append(True)
                    accesslist = "1"+accesslist
                    mlogger.debug("appending true ...... "+str(forum.id))
                    jumpflag = True
                    break
        
          #already one group has acces to forum no need to check whether other groups have access to it or not        
            if jumpflag:
               mlogger.debug("breaking up"+str(jumpflag)) 
               break
        
        if jumpflag == False:
            mlogger.debug("appending false.........."+str(forum.id))
            accesslist = "0"+accesslist
            
   
    mlogger.debug("what is the accesslist "+accesslist)
    totaltopics = Ftopics.objects.count()
    totalposts = totaltopics + Reply.objects.count()
    totalusers =  User.objects.count()
    import datetime
    now = datetime.datetime.now()
    users_online = DinetteUserProfile.objects.filter(last_activity__gte =  now - datetime.timedelta(seconds = 900)).count()
    last_registered_user = User.objects.order_by('-date_joined')[0]
    try:
        user_access_list = int(accesslist)
    except ValueError:
        user_access_list = 0
    payload = {'users_online':users_online, 'forums_list':forums,'totaltopics':totaltopics,
               'totalposts':totalposts,'totalusers':totalusers,'user_access_list':user_access_list,
               'last_registered_user':last_registered_user}
    return render_to_response("dinette/mainindex.html", payload,RequestContext(request))



def welcomePage(request, categoryid,  pageno=1) :
    mlogger.info("In the welcome page.......................")
    mlogger.debug("Type of request.user %s" % type(request)  )   
    #buid a form for posting topics
    topicform = FtopicForm()
    category = Category.objects.get(pk=categoryid)
    queryset = Ftopics.objects.filter(category__id__exact = categoryid)    
    paginator = Paginator(queryset,settings.TOPIC_PAGE_SIZE)
    topiclist = paginator.page(pageno)
    return render_to_response("dinette/home.html", {'topicform': topicform,'category':category,'authenticated':request.user.is_authenticated(),'topic_list':topiclist},RequestContext(request))
    
    
       
def topic_list(request):
    queryset = Ftopics.objects.all()                
    return object_list(request, queryset = queryset, template_name = 'dinette/topiclist.html', template_object_name='topic', paginate_by=2)
    
def topic_detail(request, topic_id , pageno = 1):
    topic = Ftopics.objects.get(pk = topic_id)
    #some body has viewed th is topic
    topic.viewcount = topic.viewcount + 1
    topic.save()
    #we also need to display the reply form
    paginator = Paginator(topic.reply_set.all(),settings.REPLY_PAGE_SIZE)
    replylist = paginator.page(pageno)
    replyform = ReplyForm()
    payload = {'topic': topic,'replyform':replyform,'reply_list':replylist}
    return render_to_response("dinette/topic_detail.html", payload, RequestContext(request))

@login_required
def postTopic(request) :
    mlogger.info("In post Topic page.....................")
    mlogger.debug("Type of request.user %s" % type(request.user)  )
    
    topic = FtopicForm(request.POST,request.FILES)
   
    if topic.is_valid() == False :
        d = {"is_valid":"false","response_html":topic.as_table()}
        json = simplejson.dumps(d)
        if request.FILES :
            json = "<textarea>"+simplejson.dumps(d)+"</textarea>"
        else:
            json = simplejson.dumps(d)
        return HttpResponse(json)                    
     
     
    #code which checks for flood control
    if (datetime.now() -(request.user.get_profile().last_posttime)).seconds <= settings.FLOOD_TIME :
    #oh....... user trying to flood us Stop him
         d2 = {"is_valid":"flood","errormessage":"Flood control.................."}
         if request.FILES : 
               json = "<textarea>"+simplejson.dumps(d2)+"</textarea>"
         else :
               json = simplejson.dumps(d2)  
         return HttpResponse(json)
         
    ftopic = topic.save(commit=False)     
    #only if there is any file
    if request.FILES :
        if(request.FILES['file'].content_type.find("image") >= 0 ) :
            ftopic.attachment_type = "image"
        else :
            ftopic.attachment_type = "text"
        ftopic.filename = request.FILES['file'].name
        
    ftopic.posted_by = request.user
    mlogger.debug("categoryid= %s" %request.POST['categoryid'])
    ftopic.category  = Category.objects.get(pk = request.POST['categoryid'])
    #Assigning user rank
    mlogger.debug("Assigning an user rank and last posted datetime")     
    assignUserElements(request.user)
    ftopic.save()
    mlogger.debug("what is the message (%s %s) " % (ftopic.message,ftopic.subject))    
    payload = {'topic':ftopic}
    response_html = render_to_string('dinette/topic_detail_frag.html', payload,RequestContext(request))
    mlogger.debug("what is the response = %s " % response_html)
  
    d2 = {"is_valid":"true","response_html":response_html}
    #this the required for ajax file uploads
    if request.FILES : 
       json = "<textarea>"+simplejson.dumps(d2)+"</textarea>"
    else :
       json = simplejson.dumps(d2) 
    return HttpResponse(json)
    
@login_required    
def postReply(request) :
    mlogger.info("in post reply.................")
    freply = ReplyForm(request.POST,request.FILES)
    
    if freply.is_valid() == False :
        d = {"is_valid":"false","response_html":freply.as_table()}
        json = simplejson.dumps(d)
        if request.FILES :
            json = "<textarea>"+simplejson.dumps(d)+"</textarea>"
        else:
            json = simplejson.dumps(d)
        return HttpResponse(json)
        
        
        
    #code which checks for flood control
    if (datetime.now() -(request.user.get_profile().last_posttime)).seconds <= settings.FLOOD_TIME:
    #oh....... user trying to flood us Stop him
         d2 = {"is_valid":"flood","errormessage":"Flood control.................."}
         if request.FILES : 
               json = "<textarea>"+simplejson.dumps(d2)+"</textarea>"
         else :
               json = simplejson.dumps(d2)  
         return HttpResponse(json)        
        
    
    reply = freply.save(commit=False)    
     #only if there is any file
    if len(request.FILES.keys()) == 1 :
        if(request.FILES['file'].content_type.find("image") >= 0 ) :
            reply.attachment_type = "image"
        else :
            reply.attachment_type = "text"
            
        reply.filename = request.FILES['file'].name
        
    reply.posted_by = request.user
    mlogger.debug("toipcid= %s" %request.POST['topicid'])
    reply.topic = Ftopics.objects.get(pk = request.POST['topicid'])
    #Assigning user rank
    mlogger.debug("Assigning an user rank, and last posted datetime")
    assignUserElements(request.user) 
    reply.save()
    payload = {'reply':reply}    
    mlogger.debug("what is the replymesage = %s" %reply.message)
    response_html = render_to_string('dinette/replydetail_frag.html', payload ,RequestContext(request))
    mlogger.debug("what is the response = %s " % response_html)
    
    d2 = {"is_valid":"true","response_html":response_html}
        
    if request.FILES :
        #this the required for ajax file uploads
        json = "<textarea>"+simplejson.dumps(d2)+"</textarea>"
    else:
        json = simplejson.dumps(d2)
    
    return HttpResponse(json)  
    
    
    
class LatestTopicsByCategory(Feed):
     title_template = 'dinette/feeds/title.html'
     description_template = 'dinette/feeds/description.html'

     def get_object(self, whichcategory):
         mlogger.debug("Feed for category %s " % whichcategory)
         return Category.objects.get(pk=whichcategory[0])
         
     def title(self, obj):
        return "Latest topics in category %s" % obj.name
     
     def link(self, obj):
        return  settings.SITE_URL

     def items(self, obj):
        return obj.ftopics_set.all()[:10]
       
     #construct these links by means of reverse lookup  by
     #using permalink decorator
     def item_link(self,obj):
        return  obj.get_absolute_url()
     
     def item_pubdate(self,obj):
        return obj.created_on
    
    
class LatestRepliesOfTopic(Feed):
     title_template = 'dinette/feeds/title.html'
     description_template = 'dinette/feeds/description.html'

     def get_object(self, whichtopic):
         mlogger.debug("Feed for category %s " % whichtopic)
         return Ftopics.objects.get(pk=whichtopic[0])
         
     def title(self, obj):
        return "Latest replies in topic %s" % obj.subject
     
     def link(self, obj):
        return  settings.SITE_URL

     def items(self, obj):
        list = []
        list.insert(0,obj)
        for obj in obj.reply_set.all()[:10] :
            list.append(obj)           
        return list
       
     #construct these links by means of reverse lookup  by
     #using permalink decorator
     def item_link(self,obj):       
        return  obj.get_absolute_url()
     
     def item_pubdate(self,obj):
        return obj.created_on
    
    
    
def assignUserElements(user):
    rank = ""
    totalposts = user.ftopics_set.count() + user.reply_set.count()
    if( totalposts > 0 and totalposts <= 30 ):
        rank = "Memeber"
    elif totalposts > 30 and totalposts < 700   :
        rank = "Senior Memeber"
    elif totalposts >= 700 :
        rank = "Star"
        
    userprofile = user.get_profile()
    userprofile.userrank = rank
    #this is the time when user posted his last post
    userprofile.last_posttime = datetime.now()
    userprofile.save()
    