#Auto created tests via DJango test utils

from django.test import TestCase
from django.test import Client
from django import template
from django.db.models import get_model

class Testmaker(TestCase):

    fixtures = ["dinette_testmaker"]

    def setUp(self):
        self.client = Client()

    def test_index_page(self):
        r = self.client.get('/forum/', {})
        self.assertEqual(r.status_code, 200)

           
    def test_forumpost_reply(self):
        r = self.client.post('/forum/post/reply/', {'topicid': '7', 'message': 'Hello', 'authenticated': 'True', 'file': '', })
        self.assertEqual(r.statuscode,200)
    

    def test_forumpost_topic(self):
        r = self.client.post('/forum/post/topic/', {'message': '2', 'authenticated': 'True', 'categoryid': '7', 'file': '', 'subject': '2', })
        self.assertEqual(r.status_code, 200)
    


    
    

