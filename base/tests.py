from .models import GAF, Organism, RefSeq, Gene
from .views import GAFViewSet, UserViewSet
import json
from django import forms
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.test import force_authenticate


class ApiPermissionsTestCase(TestCase):
    """
    TODO: fix to represent new data structures
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser('jane', 'j.doe@tamu.edu', 'password')
        self.regularuser = User.objects.create_user('alice', 'a.doe@tamu.edu', 'password')
        self.client = APIClient()
        self.client.login(username='jane', password='password')

        organism = Organism.objects.create(common_name="Miro", taxon="12345", ebi_id="L12345")
        refseq = RefSeq.objects.create(name='Miro.1', length='20000', organism=organism)
        gene = Gene.objects.create(start=100, end=500, strand=1, refseq=refseq, db_object_id="idk", db_object_symbol="idk2")



        self.gaf_obj = {
            'db': 'PMID',
            'go_id': '01234',
            'db_reference': '12345',
            'evidence_code': 'ECO:0000123',
            'aspect': 'P',
            'date': '2016-01-01T01:01:01Z',
            'assigned_by': 'CPT',
            'gene': {
                'id': str(gene.id),
            },
        }

    def deep_sort(self, obj):
        """
        Recursively sort list or dict nested lists

        http://stackoverflow.com/questions/18464095/how-to-achieve-assertdictequal-with-assertsequenceequal-applied-to-values/27949519#27949519
        """

        if isinstance(obj, dict):
            _sorted = {}
            for key in sorted(obj):
                _sorted[key] = self.deep_sort(obj[key])

        elif isinstance(obj, list):
            new_list = []
            for val in obj:
                new_list.append(self.deep_sort(val))
            _sorted = sorted(new_list)

        else:
            _sorted = obj

        return _sorted

    def test_GetUsers(self):
        response = self.client.get('/users/')
        GOOD = """{"count":2,"next":null,"previous":null,"results":[{"id":1,"username":"jane","email":"j.doe@tamu.edu","group":[]},{"id":2,"username":"alice","email":"a.doe@tamu.edu","group":[]}]}"""
        good_data = self.deep_sort(json.loads(GOOD))
        resp_data = self.deep_sort(json.loads(response.content))
        self.assertEqual(good_data, resp_data)

    def test_GafCreation(self):
        self.client.login(username='jane', password='password')
        response = self.client.get('/gafs/')
        self.assertEqual(response.content, '{"count":0,"next":null,"previous":null,"results":[]}')
        response = self.client.post('/gafs/', self.gaf_obj, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GAF.objects.count(), 1)

    def test_GafDeletion(self):
        self.client.login(username='jane', password='password')
        self.assertEqual(GAF.objects.count(), 0)
        response = self.client.post('/gafs/', self.gaf_obj, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GAF.objects.count(), 1)
        response = self.client.delete('/gafs/' + GAF.objects.all()[0].id.hex + '/', data=self.gaf_obj, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(GAF.objects.count(), 0)

    def test_GafDeletionByNonSelf(self):
        self.client.login(username='jane', password='password')
        self.assertEqual(GAF.objects.count(), 0)
        response = self.client.post('/gafs/', self.gaf_obj, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GAF.objects.count(), 1)

        self.client.login(username='alice', password='password')
        response = self.client.delete('/gafs/' + GAF.objects.all()[0].id.hex + '/', data=self.gaf_obj, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(GAF.objects.count(), 1)
