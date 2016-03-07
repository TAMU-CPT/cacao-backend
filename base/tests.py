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
        self.assertEqual(response.content, '{"count":1,"next":null,"previous":null,"results":[{"id":1,"username":"jane","email":"j.doe@tamu.edu","groups":[]}]}')

    def test_GafCreation(self):
        response = self.client.get('/gafs/')
        self.assertEqual(response.content, '{"count":0,"next":null,"previous":null,"results":[]}')
        response = self.client.post('/gafs/', self.gaf_obj)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GAF.objects.count(), 1)


class CreateGAFTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('jane', 'j.doe@tamu.edu', 'password')
        self.client = APIClient()
        self.client.login(username='jane', password='password')
        self.data = {
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
        self.factory = APIRequestFactory()

    def test_can_create_gaf(self):
        response = self.client.post('/gafs/', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



class CreateUserTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.data = {'username': 'mike', 'first_name': 'Mike', 'last_name': 'Tyson'}

    def test_can_create_user(self):
        response = self.client.post('/users/', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReadUserTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.user = User.objects.create(username="mike")

    def test_can_read_user_list(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_user_detail(self):
        response = self.client.get('/users/%d/' % self.user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteUserTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.user = User.objects.create(username="mikey")

    def test_can_delete_user(self):
        response = self.client.delete('/users/%d/' % self.user.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
