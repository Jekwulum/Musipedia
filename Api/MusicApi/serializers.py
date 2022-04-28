from django.contrib.auth.models import User
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

    class Meta:
        model = Artist
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
