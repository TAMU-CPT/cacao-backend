# from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, filters
from base.serializers import UserSerializer, GroupSerializer, GAFSerializer, ChallengeSerializer, AssessmentSerializer, PaperSerializer, OrganismSerializer, GeneSerializer, RefSeqSerializer
from base.models import GAF, Challenge, Assessment, Paper, Gene, Organism, RefSeq
from permissions import OwnerOrAdmin
from rest_framework.response import Response
import django_filters
from django.http import JsonResponse
from Bio import Entrez
import re
import stored_messages

Entrez.email = "cpt@tamu.edu"

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('username', 'email')
    ordering = ('username')

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('name', 'id')
    ordering = ('name')

class GeneFilter(filters.FilterSet):
    org_id = django_filters.CharFilter(name="refseq__organism__id")

    class Meta:
        model = Gene
        fields = ('id', 'org_id', 'db_object_id')

class GeneViewSet(viewsets.ModelViewSet):
    queryset = Gene.objects.all()
    serializer_class = GeneSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('start', 'id')
    filter_class = GeneFilter

class RefSeqViewSet(viewsets.ModelViewSet):
    queryset = RefSeq.objects.all()
    serializer_class = RefSeqSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id',)

class OrganismViewSet(viewsets.ModelViewSet):
    queryset = Organism.objects.all()
    serializer_class = OrganismSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'common_name')

class GAFFilter(filters.FilterSet):
    team = django_filters.CharFilter(name="owner__groups")

    class Meta:
        model = GAF
        fields = ('review_state', 'id', 'gene__db_object_id', 'go_id', 'db_reference', 'team', 'owner', 'gene__refseq__organism__taxon')

class GAFViewSet(viewsets.ModelViewSet):
    queryset = GAF.objects.all()
    serializer_class = GAFSerializer
    permission_classes = (OwnerOrAdmin,)
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_class = GAFFilter
    ordering_fields = ('review_state', 'id', 'owner__username', 'gene__db_object_id', 'go_id', 'db_reference', 'gene__db_object_name', 'evidence_code', 'date')
    ordering = ('date')

    def perform_create(self, serializer):
        """
        Save creater of GAF as owner on create.
        """
        gene = Gene.objects.get(id=self.request.data['gene']['id'])
        serializer.save(owner=self.request.user, gene=gene)
        stored_messages.api.add_message_for([self.request.user], stored_messages.STORED_INFO, 'yay you did it')

    def put(self, request):
        """
        Review state of GAF will change when assessed.
        """
        return self.update(request)

class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all().order_by('date')
    serializer_class = ChallengeSerializer
    permission_classes = (OwnerOrAdmin,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id',)

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all().order_by('date')
    serializer_class = AssessmentSerializer
    permission_classses = (permissions.IsAdminUser,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PaperViewSet(viewsets.ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer

    def retrieve(self, request, pk=None):
        """
        Logic for parsing paper info from PubMed using efetch
        """
        try:
            paper = Paper.objects.get(pmid=pk)
        except Paper.DoesNotExist:
            try:
                handle = Entrez.efetch("pubmed", id=str(pk), rettype="medline")

                attr = {}
                kw = ['DP', 'TI', 'TA', 'VI', 'VI', 'PG', 'AB', 'PMC']
                attr = attr.fromkeys(kw, None)
                AU = []
                MH = []

                buff = ''
                for line in handle:
                    if line.strip():
                        if line.startswith(' '):
                            buff = buff + ' ' + line.strip()
                        elif not buff:
                            buff = line.strip()
                        else:
                            key, val = buff.split('-', 1)
                            if key.strip() in kw:
                                attr[key.strip()] = val.strip()
                            elif key.strip() == 'AU':
                                AU.append(val.strip())
                            elif key.strip() == 'MH':
                                MH.append(val.strip())
                            buff = line.strip()

                attr['AU'] = ', '.join(AU)
                attr['MH'] = ', '.join(MH)
                attr['DP'] = re.sub("[^0-9]", "", attr['DP'])
                if attr['PMC']:
                    attr['PMC'] = re.sub("[^0-9]", "", attr['PMC'])

                if attr['TI']:
                    attr['TI'] = attr['TI'].strip('.')

                if attr['DP']:
                    attr['DP'] = attr['DP'][:4]

                paper = Paper(
                    pmid=pk,
                    author=attr.get('AU', None),
                    pub_year=attr.get('DP', None),
                    title=attr.get('TI', None),
                    journal=attr.get('TA', None),
                    volume=attr.get('VI', None),
                    pages=attr.get('PG', None),
                    abstract=attr.get('AB', None),
                    keywords=attr.get('MH', None),
                    pmc=attr.get('PMC', None)
                )

                handle.close()
                paper.save()
            except:
                return JsonResponse(status=404, data={'success':'false','message':'PMID:%s not found' % pk})

        serializer = PaperSerializer(paper)
        return Response(serializer.data)

@api_view(['POST'])
def mark_all_read(request):
    """
    Mark all messages as read (i.e. delete from inbox) for current logged in user
    """
    from stored_messages.settings import stored_messages_settings
    backend = stored_messages_settings.STORAGE_BACKEND()
    backend.inbox_purge(request.user)
    return Response({"message": "All messages read"})
