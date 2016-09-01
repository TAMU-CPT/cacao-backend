from django.conf.urls import url
from jbrowse import views

urlpatterns = [
    url(r'^stats/global$', views.global_stats),
    url(r'^features/Miro$', views.feature_data),
]
