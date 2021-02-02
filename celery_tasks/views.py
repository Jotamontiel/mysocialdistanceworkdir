from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import News

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
        return context

class NYTMenuPageView(TemplateView):
    template_name = "celery_tasks/displays/nytimes_display.html"

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