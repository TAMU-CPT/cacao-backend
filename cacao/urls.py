from django.conf.urls import url, include
from rest_framework import routers
from base import views
# from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'gafs', views.GAFViewSet)
router.register(r'challenges', views.ChallengeViewSet)
router.register(r'annotations', views.AnnotationViewSet)
router.register(r'assessments', views.AssessmentViewSet)

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
