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