from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

ENTRY_TYPES = (
    (0, 'Private'),
    (1, 'Public'),
    (2, 'Challenge'),
)

class Team(models.Model):
    name = models.CharField(max_length=128)
    users = models.ManyToManyField(User)

class Annotation(models.Model):
    # what is a uuid (also in challenge)?
    # what does "basically GAF2.0" mean?
    uuid = models.IntegerField()
    user = models.ForeignKey(User)

class Challenge(models.Model):
    uuid = models.IntegerField()
    user = models.ForeignKey(User)
    annotation = models.ForeignKey(Annotation)
    entry_type = models.IntegerField(choices=ENTRY_TYPES, default=0)
    date = models.DateTimeField(default=timezone.now)
    reason = models.TextField()
    # what is points/assessment?
