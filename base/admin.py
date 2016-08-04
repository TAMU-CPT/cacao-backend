from django.contrib import admin
from .models import GAF, Challenge, Assessment, Paper

class GAFAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'db', 'qualifier', 'review_state', 'go_id', 'db_reference', 'date')

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'challenge_gaf', 'original_gaf', 'date')

class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'gaf', 'challenge', 'date')

class PaperAdmin(admin.ModelAdmin):
    list_display = ('pmid', 'pub_year', 'title', 'pmc')

admin.site.register(GAF, GAFAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(Paper, PaperAdmin)
