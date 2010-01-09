#Auto created tests via DJango test utils

from django.test import TestCase
from django.test import Client
from django import template
from django.db.models import get_model

class Testmaker(TestCase):

    fixtures = ["dinette_testmaker"]


    def test_forum_126302568811(self):
        r = self.client.get('/forum/', {})
        self.assertEqual(r.status_code, 200)


    def test_forumdinette_126302582299(self):
        r = self.client.get('/forum/dinette/', {})
        self.assertEqual(r.status_code, 200)
                    
    def test_forumdinette1_126302583052(self):
        r = self.client.get('/forum/dinette/1/', {})
        self.assertEqual(r.status_code, 200)
        
        
    def test_forumpostreply_126302584183(self):
        r = self.client.post('/forum/post/reply/', {'topicid': '7', 'message': 'Hello', 'authenticated': 'True', 'file': '', })

    def test_forumdinette_126302584715(self):
        r = self.client.get('/forum/dinette/', {})
        self.assertEqual(r.status_code, 200)

    def test_forumposttopic_126302585432(self):
        r = self.client.post('/forum/post/topic/', {'message': '2', 'authenticated': 'True', 'categoryid': '7', 'file': '', 'subject': '2', })
        self.assertEqual(r.status_code, 200)