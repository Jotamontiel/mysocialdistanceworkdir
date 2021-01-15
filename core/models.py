from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Curriculum(models.Model):
    name = models.CharField(verbose_name="Curriculum Name", max_length=200, null=False, blank=False)
    tag = models.CharField(verbose_name="Curriculum Tag (Optional)", max_length=100, null=True, blank=True)
    content = RichTextField(verbose_name="Curriculum Content (Optional)", null=True, blank=True)
    uploadlink = models.FileField(upload_to='curriculums/curriculum', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated = models.DateTimeField(auto_now=True, verbose_name="Update Date")

    class Meta:
        verbose_name = "curriculum"
        verbose_name_plural = "curriculums"
        ordering = ['name']

    def __str__(self):
        return self.name