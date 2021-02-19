from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import News, LikeTradingUserBlackList, LikeTradingTicker
from .my_api_wrappers.my_api_wrapper_spotify import get_spotify_data_category
from django.db.models import Q

## TEMPORAL ##
# import requests
# from bs4 import BeautifulSoup
# import json
# from datetime import datetime
# import lxml
# from .my_api_wrappers.my_api_wrapper_nytimes import NYTAPI
# from django.conf import settings
## TEMPORAL ##

# Create your views here.
class HackerNewsDashboardView(TemplateView):
    template_name = "celery_tasks/display_hackernews/hackernews_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(HackerNewsDashboardView, self).get_context_data(**kwargs)
        context['hackernews_list'] = News.objects.all().order_by('-published')
        context['first_date'] = News.objects.all().order_by('-published').first()
        context['last_date'] = News.objects.all().order_by('published').first()
        return context

class SpotifySearchView(TemplateView):
    template_name = "celery_tasks/display_spotify/spotify_search.html"

    def get_context_data(self, **kwargs):
        context = super(SpotifySearchView, self).get_context_data(**kwargs)

        # Get query and filter from the form
        load_search_query = self.request.GET.get('q')
        load_query_filter = self.request.GET.get('filter')

        # Validation filter and set default filter
        if not load_query_filter:
            load_query_filter = 'artist'

        # Artist set context
        if load_query_filter == 'artist':           
            count, items = get_spotify_data_category(load_search_query, load_query_filter)
            context['count'] = count
            context['items'] = items
            context['q'] = load_search_query
            context['filter'] = load_query_filter

        # Track set context
        if load_query_filter == 'track':           
            count, items = get_spotify_data_category(load_search_query, load_query_filter)
            context['count'] = count
            context['items'] = items
            context['q'] = load_search_query
            context['filter'] = load_query_filter

        # Album set context
        if load_query_filter == 'album':           
            count, items = get_spotify_data_category(load_search_query, load_query_filter)
            context['count'] = count
            context['items'] = items
            context['q'] = load_search_query
            context['filter'] = load_query_filter

        # Playlist set context
        if load_query_filter == 'playlist':           
            count, items = get_spotify_data_category(load_search_query, load_query_filter)
            context['count'] = count
            context['items'] = items
            context['q'] = load_search_query
            context['filter'] = load_query_filter

        return context

class LikeTradingView(TemplateView):
    template_name = "celery_tasks/display_liketrading/liketrading_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(LikeTradingView, self).get_context_data(**kwargs)
        context["tickers_list"] = LikeTradingTicker.objects.all().order_by('ticker_symbol')

        def get_ip(request):
            address = request.META.get('HTTP_X_FORWARDED_FOR')
            if address:
                ip = address.split(',')[-1].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip

        ip=get_ip(self.request)
        myuser=LikeTradingUserBlackList(user_ip=ip)
        result=LikeTradingUserBlackList.objects.filter(Q(user_ip__icontains=ip))

        if len(result)==1:
            print("Usuario ya existe")

        elif len(result)>1:
            print("Usuario ya existe mas...")

        else:
            myuser.save()
            print("Usuario unico, ahora guardado en la blacklist")

        context["users_list"] = LikeTradingUserBlackList.objects.all()
        context["users_count"] = LikeTradingUserBlackList.objects.all().count()
        
        return context

class NYTMenuPageView(TemplateView):
    template_name = "celery_tasks/display_nytimesnews/nytimesnews_dashboard.html"

    # def get_context_data(self, **kwargs):
    #     context = super(NYTMenuPageView, self).get_context_data(**kwargs)

    #     nyt = NYTAPI(settings.NYTIMES_APP_KEY, https=False)
    #     most_viewed = nyt.most_viewed()

    #     article_list = []
    #     r = requests.get('https://news.ycombinator.com/rss')
    #     soup = BeautifulSoup(r.content, features='xml')
    #     articles = soup.findAll('item')
    #     for a in articles:
    #         title = a.find('title').text
    #         link = a.find('link').text
    #         published_wrong = a.find('pubDate').text
    #         published = datetime.strptime(published_wrong, '%a, %d %b %Y %H:%M:%S %z')
    #         article = {
    #             'title': title,
    #             'link': link,
    #             'published': published,
    #             'source': 'HackerNews RSS'
    #         }
    #         article_list.append(article)

    #     print("Hola mundo 1: ", most_viewed)
    #     print("Hola mundo 2: ", article_list)


    #     return context