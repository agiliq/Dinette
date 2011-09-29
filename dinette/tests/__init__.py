#Auto created tests via DJango test utils

from django.test import TestCase
from django.test import Client
from django import template
from django.db.models import get_model

class Testmaker(TestCase):
    fixtures = ['test_data']

    def setUp(self):
        self.client = Client()

    def test_index_page(self):
        r = self.client.get('/forum/', {})
        self.assertEqual(r.status_code, 200)
        

           



    


    
    

