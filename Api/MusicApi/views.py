from django.http import Http404
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.authtoken.models import Token
# from Api import models
from Api.models import Album, Artist, Song
from .serializers import (AlbumSerializer, ArtistSerializer,
                          SongSerializer, UserSerializer)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(data={'message': 'logout successful'}, status=status.HTTP_200_OK)


class ArtistListAV(APIView):
    def get(self, request):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ArtistDetailAV(APIView):
    def get_object(self, pk, stage_name):
        try:
            if pk:
                return Artist.objects.get(pk=pk)
            elif stage_name:
                return Artist.objects.get(stage_name=stage_name)
        except Artist.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, stage_name=None):
        artist = self.get_object(pk, stage_name)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

    def patch(self, request, pk=None, stage_name=None):
        artist = self.get_object(pk, stage_name)
        serializer = ArtistSerializer(artist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, stage_name=None):
        artist = self.get_object(pk, stage_name)
        serializer = ArtistSerializer(artist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, stage_name=None):
        artist = self.get_object(pk, stage_name)
        artist.delete()
        return Response({'message': 'Deleted'}, status.HTTP_204_NO_CONTENT)


class AlbumListAV(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AlbumDetailAV(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SongListAV(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SongDetailAV(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UserCreateAV(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "Registration Successful!"
            data['username'] = user.username

            # token = Token.objects.get(user=user).key
            # data['token'] = token

            data['token'] = get_tokens_for_user(user)

        else:
            data = serializer.errors

        return Response(data)


class UserListAV(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetailAV(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
