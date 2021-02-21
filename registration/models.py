from django.db import models
from django.contrib.auth.models import User
# from django.dispatch import receiver
# from django.db.models.signals import post_save

def avatar_custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/avatar_photo/' + filename

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickName = models.CharField(verbose_name="Nick Name", max_length=400, null=False, blank=False)
    avatar = models.ImageField(verbose_name="Profile Image", upload_to=avatar_custom_upload_to, blank=True)
    rut = models.CharField(verbose_name="Profile Rut", max_length=50, null=False, blank=False, unique=True)
    birthDate = models.DateField(verbose_name="Profile Birthday", null=True, blank=True)
    gender = models.CharField(verbose_name="Profile Gender", max_length=20, null=True, blank=True)
    position = models.CharField(verbose_name="Profile Company Position", max_length=100, null=True, blank=True)
    workPhone = models.CharField(verbose_name="Profile Work Phone", max_length=100, null=True, blank=True)
    phone = models.CharField(verbose_name="Profile Phone", max_length=100, null=True, blank=True)
    nationality = models.CharField(verbose_name="Profile Nationality", max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated = models.DateTimeField(auto_now=True, verbose_name="Update Date")

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"
        ordering = ['user__username']
    
    def __str__(self):
        return self.nickName

# @receiver(post_save, sender=User)
# def ensure_profile_exists(sender, instance, **kwargs):
#     if kwargs.get('created', False):
#         Profile.objects.get_or_create(user=instance)
#         print("Se acaba de crear un usuario y su perfil enlazado")