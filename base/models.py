from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import uuid


ENTRY_TYPES = (
    (0, 'Private'),
    (1, 'Public'),
    (2, 'Challenge'),
)

REVIEW_STATE = (
    (0, 'External'),
    (1, 'Unreviewed'),
    (2, 'Accepted'),
    (3, 'Rejected'),
)

class GAF(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, null=True)
    review_state = models.IntegerField(choices=REVIEW_STATE, default=0)
    db = models.CharField(max_length=64)
    db_object_id = models.CharField(max_length=64)
    db_object_symbol = models.CharField(max_length=64)
    qualifier = models.CharField(blank=True, max_length=64)
    go_id = models.CharField(max_length=64)
    db_reference = models.CharField(max_length=64)
    evidence_code = models.CharField(max_length=64)
    with_or_from = models.CharField(default = '', blank=True, max_length=64)
    aspect = models.CharField(max_length=64)
    db_object_name = models.CharField(default = '', blank=True, max_length=64)
    db_object_synonym = models.CharField(default = '', blank=True, max_length=64)
    db_object_type = models.CharField(max_length=64)
    taxon = models.CharField(max_length=64)
    date = models.DateField(auto_now_add=True)
    assigned_by = models.CharField(max_length=64)
    annotation_extension = models.CharField(default = '', blank=True, null=True, max_length=64)
    gene_product_id = models.CharField(default = '', blank=True, null=True, max_length=64)
    notes = models.TextField(default='')

    class Meta:
        unique_together = ('db', 'db_object_id', 'go_id', 'db_reference', 'evidence_code', 'taxon')

    def __str__(self):
        return str(self.id)

class Challenge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('auth.User')
    challenge_gaf = models.ForeignKey(GAF, related_name="challenge_gaf")
    original_gaf = models.ForeignKey(GAF, related_name="original_gaf")
    entry_type = models.IntegerField(choices=ENTRY_TYPES, default=0)
    date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()

    def __str__(self):
        return str(self.id)

class Assessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gaf = models.ForeignKey(GAF, null=True, blank=True)
    challenge = models.ForeignKey(Challenge, null=True, blank=True)
    flagged = models.TextField(blank=True, null=True)
    notes = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

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

    def __str__(self):
        return 'PMID:%s' % self.pmid
