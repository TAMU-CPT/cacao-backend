from django.contrib.auth.models import User, Group
from rest_framework import serializers
from base.models import GAF, Challenge, Assessment, Paper, Gene, Organism, RefSeq
from django.db import IntegrityError
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
        email = obj.email.lower().encode('utf-8')
        return hashlib.md5(email).hexdigest()

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

class AssessmentSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SerializerMethodField()
    class Meta:
        model = Assessment
        fields = ('owner', 'gaf', 'id', 'challenge', 'flagged', 'notes', 'date')

    def get_owner(self, obj):
        return GrouplessUserSerializer(obj.owner).data

class ChallengeSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SerializerMethodField()
    assessment = AssessmentSerializer(read_only=True, allow_null=True)
    class Meta:
        model = Challenge
        fields = ('owner', 'id', 'challenge_gaf', 'original_gaf', 'entry_type', 'date', 'reason', 'assessment')

    def get_owner(self, obj):
        return GrouplessUserSerializer(obj.challenge_gaf.owner).data

class AssessmentlessChallengeSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SerializerMethodField()
    class Meta:
        model = Challenge
        fields = ('owner', 'id', 'challenge_gaf', 'original_gaf', 'entry_type', 'date', 'reason')

    def get_owner(self, obj):
        return GrouplessUserSerializer(obj.challenge_gaf.owner).data

class OrganismSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organism
        fields = ('id', 'common_name', 'taxon', 'ebi_id')


class RefSeqSerializer(serializers.ModelSerializer):

    class Meta:
        model = RefSeq
        fields = ('id', 'name', 'organism', 'length')

    # def create(self, validated_data):
        # print(validated_data)

class GeneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gene
        fields = ('id', 'start', 'end', 'strand', 'refseq', 'db_object_id', 'db_object_symbol', 'db_object_name', 'db_object_synonym', 'db_object_type', 'gene_product_id', 'alternate_name')

    def create(self, vd):
        vd['id'] = vd['db_object_id']
        try:
            obj = super(GeneSerializer, self).create(vd)
            return obj
        except IntegrityError:
            return Gene.objects.get(id=vd['id'])

class GAFSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SerializerMethodField()
    challenge_gaf=AssessmentlessChallengeSerializer(read_only=True, allow_null=True)
    original_gaf=ChallengeSerializer(many=True, read_only=True, allow_null=True)
    assessment=AssessmentSerializer(read_only=True, allow_null=True)
    gene=GeneSerializer(read_only=True)

    class Meta:
        model = GAF
        fields = ('owner',
                  'review_state',
                  'id',
                  'db',
                  'gene',
                  'qualifier',
                  'go_id',
                  'db_reference',
                  'evidence_code',
                  'with_or_from',
                  'aspect',
                  'date',
                  'assigned_by',
                  'annotation_extension',
                  'notes',
                  'challenge_gaf',
                  'original_gaf',
                  'assessment',
                  'superseded')

    def get_owner(self, obj):
        return GrouplessUserSerializer(obj.owner).data

class PaperSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Paper
        fields = ('pmid', 'author', 'pub_year', 'title', 'journal', 'volume', 'pages', 'abstract', 'keywords', 'pmc')
