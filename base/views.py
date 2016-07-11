# from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from base.serializers import UserSerializer, GroupSerializer, GAFSerializer, AnnotationSerializer, ChallengeSerializer, AssessmentSerializer, PaperSerializer
from base.models import GAF, Annotation, Challenge, Assessment, Paper
from permissions import OwnerOrAdmin
from rest_framework.response import Response
from django.http import JsonResponse
from Bio import Entrez
import re

Entrez.email = "cpt@tamu.edu"

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-username')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GAFViewSet(viewsets.ModelViewSet):
    queryset = GAF.objects.all()
    serializer_class = GAFSerializer
    permission_classes = (OwnerOrAdmin,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all().order_by('-date')
    serializer_class = ChallengeSerializer
    permission_classes = (OwnerOrAdmin,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all().order_by('-date')
    serializer_class = AnnotationSerializer
    permission_classes = (OwnerOrAdmin,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all().order_by('-date')
    serializer_class = AssessmentSerializer
    permission_classses = (permissions.IsAdminUser,)

class PaperViewSet(viewsets.ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer

    def retrieve(self, request, pk=None):
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

                paper = Paper(
                    pmid=pk,
                    author=attr['AU'],
                    pub_year=attr['DP'],
                    title=attr['TI'],
                    journal=attr['TA'],
                    volume=attr['VI'],
                    pages=attr.get('PG', None),
                    abstract=attr['AB'],
                    keywords=attr['MH'],
                    pmc=attr.get('PMC', None)
                )

                handle.close()
                paper.save()
            except:
                return JsonResponse(status=404, data={'status':'false','message':'PMID:%s not found' % pk})

        serializer = PaperSerializer(paper)
        return Response(serializer.data)
