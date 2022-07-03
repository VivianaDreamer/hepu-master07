from django.contrib import admin
from .models import Pages, Patch

class PagesAdmin(admin.ModelAdmin):
    readonly_fields = ('created','updated')
    search_fields = ('title', 'content')

class PatchAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    search_fields = ('changes', 'notes', 'version')

# Register your models here.
admin.site.register(Pages, PagesAdmin)
admin.site.register(Patch, PatchAdmin)