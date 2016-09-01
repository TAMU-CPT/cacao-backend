from django.conf.urls import url, include
from rest_framework import routers
from base import views
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'gafs', views.GAFViewSet)
router.register(r'challenges', views.ChallengeViewSet)
router.register(r'assessments', views.AssessmentViewSet)
router.register(r'papers', views.PaperViewSet)
router.register(r'genes', views.GeneViewSet)
router.register(r'organisms', views.OrganismViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/','rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^api-token-refresh/', 'rest_framework_jwt.views.refresh_jwt_token'),
    url(r'^api-token-verify/', 'rest_framework_jwt.views.verify_jwt_token'),
    url(r'^api/', include('stored_messages.urls')),
    url(r'^mark_all_read/$', views.mark_all_read, name='mark_all_read'),
]
