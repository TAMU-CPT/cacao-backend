from django.conf.urls import url
from jbrowse import views

urlpatterns = [
    url(r'^stats/global$', views.global_stats),
    url(r'^features/(?P<name>.+)$', views.feature_data),
    url(r'^remap$', views.remap_to_new_build),
]
