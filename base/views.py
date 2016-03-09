# from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from base.serializers import UserSerializer, GroupSerializer, GAFSerializer, AnnotationSerializer, ChallengeSerializer, AssessmentSerializer
from base.models import GAF, Annotation, Challenge, Assessment
from permissions import UserPermissions

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-username')
    serializer_class = UserSerializer
    permission_classes = (UserPermissions,)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GAFViewSet(viewsets.ModelViewSet):
    queryset = GAF.objects.all()
    serializer_class = GAFSerializer
    permission_classes = (UserPermissions,)

class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all().order_by('-date')
    serializer_class = ChallengeSerializer

class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all().order_by('-date')
    serializer_class = AnnotationSerializer

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all().order_by('-date')
    serializer_class = AssessmentSerializer
