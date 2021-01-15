from django.contrib import admin
from .models import Curriculum

# Register your models here.
class CurriculumAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('name', 'tag', 'updated', 'created')
    ordering = ('name', 'tag', 'created')
    search_fields = ('name', 'tag')
    
    class Media:
        css = {
            'all': ('services/css/custom_ckeditor.css',)
        }

admin.site.register(Curriculum, CurriculumAdmin)