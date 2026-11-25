from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch
from .populate import initiate

class DealershipTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='testdriver',password='ExamplePass!123')
    def test_authentication(self):
        response=self.client.post('/djangoapp/login',{'userName':'testdriver','password':'ExamplePass!123'},content_type='application/json')
        self.assertEqual(response.json()['status'],'Authenticated')
        self.assertEqual(self.client.get('/djangoapp/logout').status_code,200)
    def test_cars(self):
        initiate()
        self.assertTrue(self.client.get('/djangoapp/get_cars').json()['CarModels'])
    @patch('djangoapp.views.get_request',return_value=[{'id':1,'state':'Kansas'}])
    def test_dealers(self,mock):
        self.assertEqual(self.client.get('/djangoapp/get_dealers/Kansas').json()['dealers'][0]['state'],'Kansas')
        mock.assert_called_once_with('fetchDealers/Kansas')
