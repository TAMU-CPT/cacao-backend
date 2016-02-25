from django.contrib.auth.models import User, Group
from rest_framework import serializers
from base.models import GAF, Annotation, Challenge, Assessment

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

class GAFSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GAF
        fields = ('db',
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
                  'gene_product_id')

class AnnotationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Annotation
        fields = ('uuid', 'gaf', 'user', 'date')

class ChallengeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Challenge
        fields = ('uuid', 'user', 'annotation', 'gaf', 'entry_type', 'date', 'reason')

class AssessmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Assessment
        fields = ('annotation', 'challenge', 'flagged', 'notes', 'date')
