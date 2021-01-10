from django.db import models
from ckeditor.fields import RichTextField

class ServiceVideo(models.Model):
    name = models.CharField(verbose_name="Video Name", max_length=200, null=False, blank=False)
    tag = models.CharField(verbose_name="Video Tag (Optional)", max_length=100, null=True, blank=True)
    description = RichTextField(verbose_name="Video Description (Optional)", null=True, blank=True)
    link = models.URLField(verbose_name="Video Link", max_length=600, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated = models.DateTimeField(auto_now=True, verbose_name="Update Date")
        
    class Meta:
        verbose_name = "service video"
        verbose_name_plural = "service videos"
        ordering = ['tag', 'name']

    def __str__(self):
        return self.name

class ServiceImage(models.Model):
    name = models.CharField(verbose_name="Image Name", max_length=200, null=False, blank=False)
    tag = models.CharField(verbose_name="Image Tag (Optional)", max_length=100, null=True, blank=True)
    link = models.URLField(verbose_name="Image Link (Optional)", max_length=600, null=True, blank=True)
    uploadlink = models.ImageField(verbose_name="Upload Image (1920x1080 px, Optional)", upload_to="services/service", blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated = models.DateTimeField(auto_now=True, verbose_name="Update Date")
    
    class Meta:
        verbose_name = "service image"
        verbose_name_plural = "service images"
        ordering = ['tag', 'name']

    def __str__(self):
        return self.name

class Service(models.Model):
    title = models.CharField(verbose_name="Service Title", max_length=200, null=False, blank=False)
    subtitle = models.CharField(max_length=200, verbose_name="Service Sub-Title (Optional)", null=True, blank=True)
    tag = models.CharField(verbose_name="Service Tag (Optional)", max_length=100, null=True, blank=True)
    summary = RichTextField(verbose_name="Service Summary (Optional)", null=True, blank=True)
    content = RichTextField(verbose_name="Service Content (Optional)", null=True, blank=True)
    order = models.SmallIntegerField(verbose_name="Service Order (Optional)", default=0)
    video = models.ManyToManyField(ServiceVideo, verbose_name="Service Videos (Optional)", null=True, blank=True)
    image = models.ManyToManyField(ServiceImage, verbose_name="Service Images (Optional)", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated = models.DateTimeField(auto_now=True, verbose_name="Update Date")

    class Meta:
        verbose_name = "service"
        verbose_name_plural = "services"
        ordering = ['title']

    def __str__(self):
        return self.title

class Employer(models.Model):
    name = models.CharField(max_length=200, verbose_name="Employer Name", null=False, blank=False)
    content = RichTextField(verbose_name="Employer Description (Optional)", null=True, blank=True)
    logoimage = models.ImageField(verbose_name="Employer Logo (400x300 px)", upload_to="services/employer")
    lat = models.FloatField(verbose_name="Employer Latitude (Optional)", null=True, blank=True)
    lon = models.FloatField(verbose_name="Employer Longitude (Optional)", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated = models.DateTimeField(auto_now=True, verbose_name="Update Date")

    class Meta:
        verbose_name = "employer"
        verbose_name_plural = "employers"
        ordering = ['name']
    
    def __str__(self):
        return self.name