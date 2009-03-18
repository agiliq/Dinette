from django.forms import ModelForm

from dinette.models import Ftopics ,Reply

#create a form from this Ftopics and use this when posting the a Topic
class FtopicForm(ModelForm):
      class Meta:
            model = Ftopics
            fields = ('subject', 'message','file' )
            

#create a form from Reply
class ReplyForm(ModelForm):
      class Meta:
            model = Reply
            fields = ('message','file')
            