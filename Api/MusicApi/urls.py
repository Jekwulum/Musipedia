from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (ArtistListAV, ArtistDetailAV,
                    AlbumListAV, AlbumDetailAV,
                    SongListAV, SongDetailAV,
                    UserCreateAV, UserListAV, UserDetailAV)

urlpatterns = [
    path('artist', ArtistListAV.as_view(), name='artist-list'),
    path('artist/<str:stage_name>', ArtistDetailAV.as_view(), name='artist-detail'),
    path('album', AlbumListAV.as_view(), name='album-list'),
    path('album/<int:pk>', AlbumDetailAV.as_view(), name='album-detail'),
    path('song', SongListAV.as_view(), name='song-list'),
    path('song/<int:pk>', SongDetailAV.as_view(), name='song-detail'),
    path('login', obtain_auth_token, name='login'),
    path('register', UserCreateAV.as_view(), name='register'),
    path('user', UserListAV.as_view(), name='user-list'),
    path('user/<int:pk>', UserDetailAV.as_view(), name='user-detail')
]
