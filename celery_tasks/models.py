from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=2083, default="", unique=True)
    published = models.DateTimeField()
    source = models.CharField(max_length=30, default="", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated = models.DateTimeField(auto_now=True, verbose_name="Update Date")

    class Meta:
        verbose_name = "news"
        verbose_name_plural = "news"
        ordering = ['title']

    def __str__(self):
        return self.title

class NYTimesNews(models.Model):
    new_id = models.IntegerField(verbose_name="ID New", default=1, unique=True)
    new_asset_id = models.IntegerField(verbose_name="ID Asset New (Optional)", default=1)
    new_URI = models.URLField(max_length=2083, verbose_name="NYTimes New URI (Optional)", default="", null=True, blank=True)
    new_URL = models.URLField(max_length=2083, verbose_name="NYTimes New URL (Optional)", default="", null=True, blank=True)
    source = models.CharField(max_length=500, verbose_name="NYTimes Source (Optional)", default="", blank=True, null=True)
    published_date = models.DateTimeField()
    section = models.CharField(max_length=500, verbose_name="NYTimes Section (Optional)", default="", blank=True, null=True)
    subsection = models.CharField(max_length=500, verbose_name="NYTimes Subsection (Optional)", default="", blank=True, null=True)
    nytdsection = models.CharField(max_length=500, verbose_name="NYTimes Ddescription (Optional)", default="", blank=True, null=True)
    adx_keywords = models.CharField(max_length=2083, verbose_name="NYTimes ADX Keywords (Optional)", default="", blank=True, null=True)
    column = models.CharField(max_length=500, verbose_name="NYTimes Column (Optional)", default="", blank=True, null=True)
    byline = models.CharField(max_length=500, verbose_name="NYTimes ByLine (Optional)", default="", blank=True, null=True)
    new_type = models.CharField(max_length=100, verbose_name="NYTimes New Type (Optional)", default="", blank=True, null=True)
    title = models.CharField(max_length=2083, verbose_name="NYTimes Title (Optional)", default="", blank=True, null=True)
    abstract = models.CharField(max_length=4083, verbose_name="NYTimes Abstract (Optional)", default="", blank=True, null=True)
    url_media_image = models.URLField(max_length=2083, verbose_name="NYTimes Media Image URL (Optional)", default="", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated = models.DateTimeField(auto_now=True, verbose_name="Update Date")

    class Meta:
        verbose_name = "nytimes_new"
        verbose_name_plural = "nytimes_news"
        ordering = ['title']

    def __str__(self):
        return self.title