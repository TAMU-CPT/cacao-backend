from django.contrib import admin
from .models import GAF, Annotation, Challenge, Assessment

admin.site.register(GAF)
admin.site.register(Annotation)
admin.site.register(Challenge)
admin.site.register(Assessment)
