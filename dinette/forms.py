from django.forms import ModelForm
from django import forms

from dinette.models import Ftopics ,Reply

#create a form from this Ftopics and use this when posting the a Topic
class FtopicForm(ModelForm):
      class Meta:
            model = Ftopics
            fields = ('subject', 'message','file' )
            

#create a form from Reply
class ReplyForm(ModelForm):
    message = forms.CharField(widget = forms.Textarea(attrs={"cols":70, "rows":8}))
    class Meta:
        model = Reply
        fields = ('message','file')
            