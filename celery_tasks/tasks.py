##################################################################################################################
################################################ CONGIGURATION TASKS SECTION #####################################
##################################################################################################################

######################################
########## INITIALIZE LIBRARIES ######
######################################
from __future__ import absolute_import, unicode_literals

######################################
########## CELERY LIBRARIES ##########
######################################
from celery import Celery
from celery import app, shared_task
from celery.utils.log import get_task_logger

######################################
########## SCRAPER LIBRARIES #########
######################################
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import lxml

######################################
########## MY API WRAPPERS ###########
######################################
from .my_api_wrappers.my_api_wrapper_nytimes import NYTAPI

######################################
########## DJANGO MODELS #############
######################################
from .models import News, NYTimesNews

######################################
########## CREDENTIALS IMPORT ########
######################################
from django.conf import settings

######################################
########## LOGGER ACTIVATION #########
######################################
logger = get_task_logger(__name__)

##################################################################################################################
################################################ TASKS SECTION ###################################################
##################################################################################################################

##############################################################
########## TASK 1: HACKER NEWS - SAVE_FUNCTION ###############
##############################################################
@shared_task(serializer='json')
def save_function(article_list):
    source = article_list[0]['source']
    new_count = 0
    error = True

    try: 
        latest_article = News.objects.filter(source=source).order_by('-id')[0]
    except Exception as e:
        print('Exception at latest_article: ')
        print(e)
        error = False
        pass
    finally:

        if error is not True:
            latest_article = None

    for article in article_list:
        
        if latest_article is None:

            try:
                News.objects.create(
                    title = article['title'],
                    link = article['link'],
                    published = article['published'],
                    source = article['source']
                )
                new_count += 1
            except Exception as e:
                print('failed at latest_article is none')
                print(e)
                break

        elif latest_article.published == None:

            try:
                News.objects.create(
                    title = article['title'],
                    link = article['link'],
                    published = article['published'],
                    source = article['source']
                )
                new_count += 1
            except:
                print('failed at latest_article.published == none')
                break

        elif latest_article.source == None:

            try:
                News.objects.create(
                    title = article['title'],
                    link = article['link'],
                    published = article['published'],
                    source = article['source']
                )
                new_count += 1
            except:
                print('failed at latest_article.source == none')
                break

        elif latest_article.published < article['published']:

            try:
                News.objects.create(
                    title = article['title'],
                    link = article['link'],
                    published = article['published'],
                    source = article['source']
                )
                new_count += 1
            except:
                print('failed at latest_article.published < j[published]')
                break

        else:
            return print('news scraping failed, date was more recent than last published date')

    logger.info(f'New articles: {new_count} articles(s) added.')
    return print('finished')

#########################################################################
########## TASK 2: HACKER NEWS - HACKERNEWS_RSS (SCRAPER) ###############
#########################################################################
@shared_task
def hackernews_rss():
    article_list = []

    try:
        r = requests.get('https://news.ycombinator.com/rss')
        soup = BeautifulSoup(r.content, features='xml')
        articles = soup.findAll('item')
        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published_wrong = a.find('pubDate').text
            published = datetime.strptime(published_wrong, '%a, %d %b %Y %H:%M:%S %z')
            article = {
                'title': title,
                'link': link,
                'published': published,
                'source': 'HackerNews RSS'
            }
            article_list.append(article)
        return save_function(article_list)
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)

#############################################################################################
########## TASK 1: NYTIMES NEWS - NYTIMESNEWS_MOSTPOPULAR_VIEWED_SAVE_FUNCTION ##############
#############################################################################################
@shared_task(serializer='json')
def nytimesnews_mostpopular_viewed_api_scraper_save_function(article_mostpopular_viewed_api_scraper_list):
    source = article_mostpopular_viewed_api_scraper_list[0]['source']
    new_count = 0
    error = True

    try: 
        latest_article = NYTimesNews.objects.filter(source=source).order_by('-id')[0]
    except Exception as e:
        print('Exception at latest_article: ')
        print(e)
        error = False
        pass
    finally:

        if error is not True:
            latest_article = None

    for article in article_mostpopular_viewed_api_scraper_list:
        
        if latest_article is None:

            try:
                NYTimesNews.objects.create(
                    new_id = article['id'],
                    new_asset_id = article['asset_id'],
                    new_URI = article['uri'],
                    new_URL = article['url'],
                    source = article['source'],
                    published_date = article['published_date'],
                    section = article['section'],
                    subsection = article['subsection'],
                    nytdsection = article['nytdsection'],
                    adx_keywords = article['adx_keywords'],
                    column = article['column'],
                    byline = article['byline'],
                    new_type = article['type'],
                    title = article['title'],
                    abstract = article['abstract']
                )
                new_count += 1
            except Exception as e:
                print('failed at latest_article is none')
                print(e)
                break

        elif latest_article.published_date == None:

            try:
                NYTimesNews.objects.create(
                    new_id = article['id'],
                    new_asset_id = article['asset_id'],
                    new_URI = article['uri'],
                    new_URL = article['url'],
                    source = article['source'],
                    published_date = article['published_date'],
                    section = article['section'],
                    subsection = article['subsection'],
                    nytdsection = article['nytdsection'],
                    adx_keywords = article['adx_keywords'],
                    column = article['column'],
                    byline = article['byline'],
                    new_type = article['type'],
                    title = article['title'],
                    abstract = article['abstract']
                )
                new_count += 1
            except:
                print('failed at latest_article.published_date == none')
                break

        elif latest_article.source == None:

            try:
                NYTimesNews.objects.create(
                    new_id = article['id'],
                    new_asset_id = article['asset_id'],
                    new_URI = article['uri'],
                    new_URL = article['url'],
                    source = article['source'],
                    published_date = article['published_date'],
                    section = article['section'],
                    subsection = article['subsection'],
                    nytdsection = article['nytdsection'],
                    adx_keywords = article['adx_keywords'],
                    column = article['column'],
                    byline = article['byline'],
                    new_type = article['type'],
                    title = article['title'],
                    abstract = article['abstract']
                )
                new_count += 1
            except:
                print('failed at latest_article.source == none')
                break

        elif latest_article.published_date.date() < article['published_date']:

            try:
                NYTimesNews.objects.create(
                    new_id = article['id'],
                    new_asset_id = article['asset_id'],
                    new_URI = article['uri'],
                    new_URL = article['url'],
                    source = article['source'],
                    published_date = article['published_date'],
                    section = article['section'],
                    subsection = article['subsection'],
                    nytdsection = article['nytdsection'],
                    adx_keywords = article['adx_keywords'],
                    column = article['column'],
                    byline = article['byline'],
                    new_type = article['type'],
                    title = article['title'],
                    abstract = article['abstract']
                )
                new_count += 1
            except:
                print('failed at latest_article.published_date < j[published_date]')
                break

        else:
            return print('The nytimesnews mostpopular viewed api scraper failed, date was more recent than last published_date date')

    logger.info(f'New articles: {new_count} articles(s) added.')
    return print('finished')

##############################################################################################
########## TASK 2: NYTIMES NEWS - NYTIMESNEWS_MOSTPOPULAR_VIEWED_API_SCRAPER #################
##############################################################################################
@shared_task
def nytimesnews_mostpopular_viewed_api_scraper():

    try:
        nyt = NYTAPI(settings.NYTIMES_APP_KEY, https=True)
        article_mostpopular_viewed_api_scraper_list = nyt.most_viewed()
        return nytimesnews_mostpopular_viewed_api_scraper_save_function(article_mostpopular_viewed_api_scraper_list)
    except Exception as e:
        print('The nytimesnews mostpopular viewed api scraper job failed. See exception:')
        print(e)