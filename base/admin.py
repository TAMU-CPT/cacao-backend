from django.contrib import admin
from .models import Team, GAF, Annotation, Challenge, Assessment

admin.site.register(Team)
admin.site.register(GAF)
admin.site.register(Annotation)
admin.site.register(Challenge)
admin.site.register(Assessment)
