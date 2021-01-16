from django.contrib import admin
from .models import News

# Register your models here.
class NewsAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated', 'published')
    list_display = ('title', 'source', 'link', 'published', 'updated', 'created')
    ordering = ('source', 'title', 'created')
    search_fields = ('title', 'source')
    
    class Media:
        css = {
            'all': ('services/css/custom_ckeditor.css',)
        }

admin.site.register(News, NewsAdmin)