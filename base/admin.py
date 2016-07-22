from django.contrib import admin
from .models import GAF, Challenge, Assessment, Paper

class GAFAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'db', 'qualifier', 'review_state', 'go_id', 'db_reference', 'date')


admin.site.register(GAF, GAFAdmin)
admin.site.register(Challenge)
admin.site.register(Assessment)
admin.site.register(Paper)
