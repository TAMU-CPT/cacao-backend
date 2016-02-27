from django.test import TestCase
from .models import GAF
from django import forms


from rest_framework.test import APIRequestFactory


class GafTestCase(TestCase):

    def test_datefield(self):
        with self.assertRaisesMessage(forms.ValidationError, 'invalid date format'):
            a = GAF.objects.create(
                db='a',
                db_object_id='a',
                db_object_symbol='a',
                qualifier='a',
                go_id='a',
                db_reference='a',
                evidence_code='a',
                with_or_from='a',
                aspect='a',
                db_object_name='a',
                db_object_synonym='a',
                db_object_type='a',
                taxon='a',
                date='a',
                assigned_by='a',
                annotation_extension='a',
                gene_product_id='a',
            )

# Using the standard RequestFactory API to create a form POST request
# factory = APIRequestFactory()
# request = factory.post('/notes/', {'title': 'new idea'})

