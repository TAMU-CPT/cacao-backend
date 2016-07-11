from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group
from multiselectfield import MultiSelectField
from uuidfield import UUIDField


ENTRY_TYPES = (
    (0, 'Private'),
    (1, 'Public'),
    (2, 'Challenge'),
)

FLAGGED = (
    (0, 'Protein'),
    (1, 'Publication'),
    (2, 'Qualifier'),
    (3, 'Go term'),
    (4, 'Evidence'),
    (5, 'Originality'),
)

class GAF(models.Model):
    owner = models.ForeignKey('auth.User')
    db = models.CharField(max_length=64)
    db_object_id = models.CharField(max_length=64)
    db_object_symbol = models.CharField(max_length=64)
    qualifier = models.CharField(max_length=64)
    go_id = models.CharField(max_length=64)
    db_reference = models.CharField(max_length=64)
    evidence_code = models.CharField(max_length=64)
    with_or_from = models.CharField(max_length=64)
    aspect = models.CharField(max_length=64)
    db_object_name = models.CharField(max_length=64)
    db_object_synonym = models.CharField(max_length=64)
    db_object_type = models.CharField(max_length=64)
    taxon = models.CharField(max_length=64)
    date = models.DateField()
    assigned_by = models.CharField(max_length=64)
    annotation_extension = models.CharField(max_length=64)
    gene_product_id = models.CharField(max_length=64)

class Annotation(models.Model):
    owner = models.ForeignKey('auth.User')
    uuid = UUIDField(auto=True)
    gaf = models.OneToOneField(GAF)
    date = models.DateTimeField(auto_now_add=True)

class Challenge(models.Model):
    owner = models.ForeignKey('auth.User')
    uuid = UUIDField(auto=True)
    annotation = models.ForeignKey(Annotation)
    gaf = models.OneToOneField(GAF)
    entry_type = models.IntegerField(choices=ENTRY_TYPES, default=0)
    date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()

class Assessment(models.Model):
    annotation = models.ForeignKey(Annotation, null=True, blank=True)
    challenge = models.ForeignKey(Challenge, null=True, blank=True)
    flagged = MultiSelectField(choices=FLAGGED, max_choices=6, default=0, blank=True)
    notes = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class Paper(models.Model):
    pmid = models.IntegerField(null=True)
    author = models.TextField(null=True)
    pub_year = models.IntegerField(null=True)
    title = models.TextField(null=True)
    journal = models.CharField(max_length=64, null=True)
    volume = models.IntegerField(null=True)
    pages = models.CharField(max_length=64, null=True)
    abstract = models.TextField(null=True)
    keywords = models.TextField(null=True)
    pmc = models.IntegerField(null=True)
