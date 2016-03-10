# from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from base.serializers import UserSerializer, GroupSerializer, GAFSerializer, AnnotationSerializer, ChallengeSerializer, AssessmentSerializer
from base.models import GAF, Annotation, Challenge, Assessment
from permissions import OwnerOrAdmin

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

class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all().order_by('-date')
    serializer_class = ChallengeSerializer
    permission_classes = (OwnerOrAdmin,)

class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all().order_by('-date')
    serializer_class = AnnotationSerializer
    permission_classes = (OwnerOrAdmin,)

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all().order_by('-date')
    serializer_class = AssessmentSerializer
    permission_classses = (permissions.IsAdminUser,)
