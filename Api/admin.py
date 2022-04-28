from django.contrib import admin
from .models import Album, Artist, Song


# Register your models here.
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('stage_name', 'full_name', 'record_label')
    list_filter = ('stage_name', )


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'created_on')
    list_filter = ('title', 'artist')


class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album')


admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
