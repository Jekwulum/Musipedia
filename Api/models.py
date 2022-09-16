from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# dob => date-of-birth; dod => date-of-death
class Artist(models.Model):
    full_name = models.CharField(max_length=200)
    stage_name = models.CharField(max_length=200, unique=True)
    record_label = models.CharField(max_length=200)
    dob = models.DateField()
    dod = models.DateField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.stage_name


class Album(models.Model):
    title = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # relations
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artist_albums')

    objects = models.Manager()

    def __str__(self):
        return self.title


class Song(models.Model):
    title = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # relations
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artist_songs')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='album_songs', null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.title
