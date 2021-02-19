from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import News, NYTimesNews, LikeTradingUserBlackList, LikeTradingTicker, LikeTradingUserVote

class TickerResource(resources.ModelResource):
    class Meta:
        model = LikeTradingTicker

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

class NYTimesNewsAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated', 'published_date')
    list_display = ('title', 'source', 'section', 'published_date', 'updated', 'created')
    ordering = ('source', 'title', 'created')
    search_fields = ('title', 'source')
    
    class Media:
        css = {
            'all': ('services/css/custom_ckeditor.css',)
        }

class LikeTradingUserBlackListAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('user_ip', 'user_alias', 'updated', 'created')
    ordering = ('user_ip', 'user_alias', 'created')
    search_fields = ('user_ip', 'user_alias')
    
    class Media:
        css = {
            'all': ('services/css/custom_ckeditor.css',)
        }

class LikeTradingTickerAdmin(ImportExportModelAdmin):
    resource_class = TickerResource
    readonly_fields = ('created', 'updated')
    list_display = ('ticker_name', 'exchange', 'updated', 'created')
    ordering = ('ticker_name', 'exchange', 'created')
    search_fields = ('ticker_name', 'exchange')
    
    class Media:
        css = {
            'all': ('services/css/custom_ckeditor.css',)
        }

class LikeTradingUserVoteAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('userblacklist_id', 'ticker_id', 'updated', 'created')
    ordering = ('userblacklist_id', 'ticker_id', 'created')
    search_fields = ('userblacklist_id', 'ticker_id')
    
    class Media:
        css = {
            'all': ('services/css/custom_ckeditor.css',)
        }

admin.site.register(News, NewsAdmin)
admin.site.register(NYTimesNews, NYTimesNewsAdmin)
admin.site.register(LikeTradingUserBlackList, LikeTradingUserBlackListAdmin)
admin.site.register(LikeTradingTicker, LikeTradingTickerAdmin)
admin.site.register(LikeTradingUserVote, LikeTradingUserVoteAdmin)