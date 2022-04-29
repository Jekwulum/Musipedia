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
