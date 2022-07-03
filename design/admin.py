from django.contrib import admin
from .models import Design, Results

# Register your models here.
class DesignAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('project_name', 'user', 'created')
    ordering = ('-created','user')
    list_filter = ('user',)

class ResultsAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

admin.site.register(Design, DesignAdmin)
admin.site.register(Results, ResultsAdmin)