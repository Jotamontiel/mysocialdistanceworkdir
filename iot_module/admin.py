from django.contrib import admin
from .models import SensorData, SensorType, Sensor, ComponentType, Component, Company

# Register your models here.
class SensorDataAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('sensor', 'value', 'updated', 'created')
    ordering = ('sensor', 'created')
    
    class Media:
        css = {
            'all': ('services/css/custom_ckeditor.css',)
        }

class SensorTypeAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('name', 'initials', 'measurementUnit', 'isGraphical', 'updated', 'created')
    ordering = ('name', 'initials', 'created')
    search_fields = ('name', 'initials', 'measurementUnit')
    
    class Media:
        css = {
            'all': ('services/css/custom_ckeditor.css',)
        }

class SensorAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('alias', 'serialCode', 'measurementUnit', 'sensorType', 'component', 'brand', 'isEnabled', 'updated', 'created')
    ordering = ('alias', 'serialCode', 'created')
    search_fields = ('alias', 'serialCode', 'measurementUnit', 'sensorType', 'component', 'brand')
    
    class Media:
        css = {
            'all': ('services/css/custom_ckeditor.css',)
        }

class ComponentTypeAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('name', 'initials', 'updated', 'created')
    ordering = ('name', 'initials', 'created')
    search_fields = ('name', 'initials')
    
    class Media:
        css = {
            'all': ('services/css/custom_ckeditor.css',)
        }

class ComponentAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('alias', 'serialCode', 'imeiRecord', 'componentType', 'profile', 'connectionType', 'supplyType', 'isEnabled', 'updated', 'created')
    ordering = ('alias', 'serialCode', 'created')
    search_fields = ('alias', 'serialCode', 'imeiRecord', 'componentType', 'profile', 'connectionType', 'supplyType')
    
    class Media:
        css = {
            'all': ('services/css/custom_ckeditor.css',)
        }

class CompanyAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('businessName', 'rut', 'street', 'number', 'office', 'city', 'profile', 'postalCode', 'email', 'updated', 'created')
    ordering = ('businessName', 'rut', 'created')
    search_fields = ('businessName', 'rut', 'street', 'number', 'office', 'city', 'profile', 'postalCode', 'email')
    
    class Media:
        css = {
            'all': ('services/css/custom_ckeditor.css',)
        }

admin.site.register(SensorData, SensorDataAdmin)
admin.site.register(SensorType, SensorTypeAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(ComponentType, ComponentTypeAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(Company, CompanyAdmin)