#Auto created tests via DJango test utils

from django.test import TestCase
from django.test import Client
from .. import models 

from django import template
from django.db.models import get_model
from django.core.urlresolvers import reverse

class Testmaker(TestCase):
    fixtures = ['test_data']

    def setUp(self):
        self.client = Client()

    def test_index_page(self):
        """Check if the homepage is accessible by all"""
        r = self.client.get(reverse('dinette_category'), {})
        self.assertEqual(r.status_code, 200)

    def test_new_topics(self):
        r = self.client.get(reverse('dinette_new_for_user'))
        #check for redirection for guest users 
        self.assertEqual(r.status_code,302)
        #check for results in case of loggedin users
        r = self.client.login(username='plaban',password='plaban') #this is in test fixture
        self.assertEqual(r,True) 
        r = self.client.get(reverse('dinette_new_for_user'))
        self.assertEqual( len(r.context['new_topic_list']),0) # as there are no entry in the db

    def test_unanswered_topics(self):
        r = self.client.get(reverse('dinette_unanswered'))
        topic =  r.context['new_topic_list'][0]
        self.assertEqual(topic.subject,'Details about the Django design patterns')
        
        
    def test_user_profile(self):
        response = self.client.get('/forum/users/plaban')
        user =  response.context['user_profile']
        self.assertEqual(user.email,'plaban.nayak@gmail.com')
    
    def test_category(self):
        response = self.client.get('/forum/dinette/')
        category =  response.context['category']
        self.assertEqual(category.name,"Dinette")
        self.assertEqual(category.description,"Dinette is the best forum app for Django, Period. You are using it right now.")
        supercategory = category.super_category
        self.assertEqual(supercategory.name,"Python and Django")
        
    def test_post_topic(self):
        response = self.client.post('/forum/post/topic/',{'subject':'python','message':'this is python','authenticated':'true','categoryid':'1'})
        print response.status_code
        response = self.client.get('/forum/active/')
        topic = response.context['new_topic_list'][0]
        self.assertEqual(topic.subject,'python')
        print topic.slug


    def test_post_reply(self):
        response = self.client.login(username = "plaban",password = "plaban")
        response = self.client.post("/forum/post/reply",{'message':'this is good','message_markup_type':'plain',
                                                         'authenticated':'True','topicid':'1'})
        self.assertEqual(response.status_code,302)
        

    def test_edit_reply(self):
        response = self.client.login(username = "plaban",password = "plaban")
        response = self.client.get("/forum/edit/reply/1")
        self.assertEqual(response.status_code,200)
        reponse = self.client.post("/forum/edit/reply/1",{'message':'this is the edit reply','message_markup_type':'plain'                                                          })
        self.assertEqual(response.status_code,200)
        reply = models.Reply.objects.all()[0]
        self.assertEqual(str(reply),'<p>this is the edit reply</p>')
        
        
        


        
    
        

        
        
        
        
        
