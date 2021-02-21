from django.contrib import admin
from .models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('nickName', 'rut', 'gender', 'position', 'nationality', 'updated', 'created')
    ordering = ('nickName', 'rut', 'created')
    search_fields = ('nickName', 'rut', 'gender', 'position', 'nationality')
    
    class Media:
        css = {
            'all': ('services/css/custom_ckeditor.css',)
        }

admin.site.register(Profile, ProfileAdmin)