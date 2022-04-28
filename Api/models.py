from django.db import models


# Create your models here.
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
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artist_albums')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.title


class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artist_songs')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='album_songs')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.title
