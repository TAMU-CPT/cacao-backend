from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
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

class Organism(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    common_name = models.CharField(max_length=128, unique=True)
    taxon = models.CharField(max_length=64)
    ebi_id = models.CharField(max_length=64)

    def __str__(self):
        return str(self.common_name)

class RefSeq(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    length = models.IntegerField()
    organism = models.ForeignKey(Organism)

    class Meta:
        unique_together = ('name', 'organism',)

    def __str__(self):
        return '%s:%s' % (self.organism.common_name, self.name)


class Gene(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start = models.IntegerField()
    end = models.IntegerField()
    strand = models.IntegerField()
    refseq = models.ForeignKey(RefSeq, null=True)
    db_object_id = models.CharField(max_length=64)
    db_object_symbol = models.CharField(max_length=64)
    gene_product_id = models.CharField(default = '', blank=True, null=True, max_length=64)
    db_object_name = models.CharField(default = '', blank=True, max_length=64)
    db_object_type = models.CharField(default='protein', max_length=64)
    db_object_synonym = models.CharField(default = '', blank=True, max_length=64)
    alternate_name = models.CharField(max_length=128, blank=True, null=True)


    def __str__(self):
        return str(self.db_object_id)

class GAF(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, null=True)
    review_state = models.IntegerField(choices=REVIEW_STATE, default=0)
    db = models.CharField(max_length=64)
    gene = models.ForeignKey(Gene, null=True)
    qualifier = models.CharField(blank=True, max_length=64)
    go_id = models.CharField(max_length=64)
    db_reference = models.CharField(max_length=64)
    evidence_code = models.CharField(max_length=64)
    with_or_from = models.CharField(default = '', blank=True, max_length=64)
    aspect = models.CharField(blank=True, max_length=64)
    date = models.DateTimeField(default=timezone.now)
    assigned_by = models.CharField(max_length=64)
    annotation_extension = models.CharField(default = '', blank=True, null=True, max_length=64)
    notes = models.TextField(default='')
    superseded = models.ForeignKey('GAF', null=True, blank=True)

    class Meta:
        unique_together = ('db', 'go_id', 'notes', 'evidence_code', 'gene')

    def __str__(self):
        return str(self.id)

class Challenge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_gaf = models.ForeignKey(GAF, related_name="original_gaf")
    challenge_gaf = models.OneToOneField(GAF, related_name="challenge_gaf", null=True, blank=True)
    entry_type = models.IntegerField(choices=ENTRY_TYPES, default=0)
    date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()

    def __str__(self):
        return str(self.id)

class Assessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('auth.User')
    gaf = models.OneToOneField(GAF, null=True, blank=True)
    challenge = models.OneToOneField(Challenge, null=True, blank=True)
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
