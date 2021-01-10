from django.contrib import admin
from .models import ServiceVideo, ServiceImage, Service, Employer

# Register your models here.
class ServiceVideoAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('name', 'tag', 'updated', 'created')
    ordering = ('name', 'tag', 'created')
    search_fields = ('name', 'tag')
    
    class Media:
        css = {
            'all': ('services/css/custom_ckeditor.css',)
        }

class ServiceImageAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('name', 'tag', 'updated', 'created')
    ordering = ('name', 'tag', 'created')
    search_fields = ('name', 'tag')
    
    class Media:
        css = {
            'all': ('services/css/custom_ckeditor.css',)
        }

class ServiceAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('title', 'subtitle', 'tag', 'updated', 'created')
    ordering = ('title', 'tag', 'created')
    search_fields = ('title', 'subtitle', 'tag')
    
    class Media:
        css = {
            'all': ('services/css/custom_ckeditor.css',)
        }

class EmployerAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('name', 'content')
    ordering = ('name', 'created')
    search_fields = ('name', 'content')
    
    class Media:
        css = {
            'all': ('services/css/custom_ckeditor.css',)
        }

admin.site.register(ServiceVideo, ServiceVideoAdmin)
admin.site.register(ServiceImage, ServiceImageAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Employer, EmployerAdmin)
