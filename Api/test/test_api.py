from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from Api.factories import (ArtistFactory, AlbumFactory)
from pprint import pprint


class APITestUtils(object):
    """
    In this class, the API URLs to be queried in the test are defined
    """

    @staticmethod
    def get_artists_url():
        return reverse('artist-list')

    @staticmethod
    def get_artist_details_url(stage_name):
        return reverse('artist-detail', kwargs={"stage_name": stage_name})

    @staticmethod
    def get_albums_url():
        return reverse('album')

    @staticmethod
    def get_album_details_url(pk):
        return reverse('album-detail', kwargs={"pk": pk})


class TestArtist(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.artists = ArtistFactory.create_batch(3)
        self.artist1 = ArtistFactory.create(
            full_name="Kirsten Dupont",
            stage_name="Kirs",
            record_label="DejaVu",
            dob="2014-08-21"
        )
        self.album1 = AlbumFactory.create(
            title="Cry me a river",
            artist=self.artist1
        )

    def test_artist_list(self):
        response = self.client.get(APITestUtils.get_artists_url())
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(len(data), 4)
        pprint(data[3]['artist_albums'])
        for artist in data:
            if artist['full_name'] == str(self.artist1.full_name):
                self.assertEqual(artist['artist_albums'][0]['title'], str(self.album1.title))
