from django.contrib.auth.models import User, Group
from rest_framework import serializers
from base.models import GAF, Challenge, Assessment, Paper
import hashlib

class UserSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'group')

    def get_group(self, obj):
        for group in obj.groups.all():
            yield BasicGroupSerializer(group).data

class GrouplessUserSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

    def get_email(self, obj):
        return hashlib.md5(obj.email.lower()).hexdigest()

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.SerializerMethodField()
    class Meta:
        model = Group
        fields = ('id', 'name', 'users')

    def get_users(self, obj):
        for user in obj.user_set.all():
            yield GrouplessUserSerializer(user).data

class BasicGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

class GAFSerializer(serializers.HyperlinkedModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    owner = serializers.SerializerMethodField()
    class Meta:
        model = GAF
        fields = ('owner',
                  'review_state',
                  'id',
                  'db',
                  'db_object_id',
                  'db_object_symbol',
                  'qualifier',
                  'go_id',
                  'db_reference',
                  'evidence_code',
                  'with_or_from',
                  'aspect',
                  'db_object_name',
                  'db_object_synonym',
                  'db_object_type',
                  'taxon',
                  'date',
                  'assigned_by',
                  'annotation_extension',
                  'gene_product_id',
                  'notes')

    def get_owner(self, obj):
        return GrouplessUserSerializer(obj.owner).data

class ChallengeSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Challenge
        fields = ('owner', 'id', 'gaf', 'entry_type', 'date', 'reason')

class AssessmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Assessment
        fields = ('gaf', 'id', 'challenge', 'flagged', 'notes', 'date')

class PaperSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Paper
        fields = ('pmid', 'author', 'pub_year', 'title', 'journal', 'volume', 'pages', 'abstract', 'keywords', 'pmc')
