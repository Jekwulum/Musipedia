from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from Api.models import Album, Artist, Song


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    album_songs = SongSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):
    artist_albums = AlbumSerializer(many=True, read_only=True)
    artist_songs = SongSerializer(many=True, read_only=True)

    @transaction.atomic
    def create(self, validated_data):
        albums_data = self.initial_data.get('albums')
        songs_data = self.initial_data.get('songs')

        instance = super().create(validated_data)
        if albums_data:
            Album.objects.bulk_create([
                Album(
                    title=album['title'],
                    artist_id=instance.id
                ) for album in albums_data
            ])
        if songs_data:
            Song.objects.bulk_create([
                Song(
                    title=song['title'],
                    artist_id=instance.id
                ) for song in songs_data
            ])

        instance = super().update(instance, validated_data)
        instance.save()
        return instance

    class Meta:
        model = Artist
        fields = '__all__'

    @transaction.atomic
    def update(self, instance, validated_data):
        albums_data = self.initial_data.get('albums')
        songs_data = self.initial_data.get('songs')

        if albums_data:
            # instance.artist_albums.clear()
            for album in albums_data:
                album_id = album.get("id")
                if album_id:
                    album_obj = Album.objects.get(id=album_id)
                    album_obj.title = album.get("title")
                    album_obj.save()
                    instance.artist_albums.add(album_obj)
                else:
                    Album.objects.create(
                        title=album.get("title"),
                        artist_id=instance.id
                    )

        if songs_data:
            # instance.artist_songs.clear()
            for song in songs_data:
                song_id = song.get("id")
                if song_id:
                    song_obj = Song.objects.get(id=song_id)
                    song_obj.title = song.get("title")
                    song_obj.save()
                    instance.artist_songs.add(song_obj)
                else:
                    Song.objects.create(
                        title=song.get("title"),
                        artist_id=instance.id
                    )

        instance = super().update(instance, validated_data)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'error': 'Passwords do not match!'})

        account = User(username=self.validated_data['username'])
        account.set_password(password)
        account.save()

        return account
