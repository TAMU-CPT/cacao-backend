from .models import GAF
from .views import GAFViewSet, UserViewSet
from django import forms
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.test import force_authenticate


class ApiPermissionsTestCase(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser('jane', 'j.doe@tamu.edu', 'password')
        self.regularuser = User.objects.create_user('alice', 'a.doe@tamu.edu', 'password')
        self.client = APIClient()
        self.client.login(username='jane', password='password')
        self.gaf_obj = {
            'db': 'a',
            'db_object_id': 'a',
            'db_object_symbol': 'a',
            'qualifier': 'a',
            'go_id': 'a',
            'db_reference': 'a',
            'evidence_code': 'a',
            'with_or_from': 'a',
            'aspect': 'a',
            'db_object_name': 'a',
            'db_object_synonym': 'a',
            'db_object_type': 'a',
            'taxon': 'a',
            'date': '2016-01-01',
            'assigned_by': 'a',
            'annotation_extension': 'a',
            'gene_product_id': 'a',
        }

    def test_GetUsers(self):
        response = self.client.get('/users/')
        self.assertEqual(response.content, '{"count":2,"next":null,"previous":null,"results":[{"id":1,"username":"jane","email":"j.doe@tamu.edu","groups":[]},{"id":2,"username":"alice","email":"a.doe@tamu.edu","groups":[]}]}')

    def test_GafCreation(self):
        self.client.login(username='jane', password='password')
        response = self.client.get('/gafs/')
        self.assertEqual(response.content, '{"count":0,"next":null,"previous":null,"results":[]}')
        response = self.client.post('/gafs/', self.gaf_obj)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GAF.objects.count(), 1)

    def test_GafDeletion(self):
        self.client.login(username='jane', password='password')
        self.assertEqual(GAF.objects.count(), 0)
        response = self.client.post('/gafs/', self.gaf_obj)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GAF.objects.count(), 1)
        response = self.client.delete('/gafs/1/', data=self.gaf_obj)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(GAF.objects.count(), 0)

    def test_GafDeletionByNonSelf(self):
        self.client.login(username='jane', password='password')
        self.assertEqual(GAF.objects.count(), 0)
        response = self.client.post('/gafs/', self.gaf_obj)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GAF.objects.count(), 1)

        self.client.login(username='alice', password='password')
        response = self.client.delete('/gafs/1/', data=self.gaf_obj)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(GAF.objects.count(), 1)
