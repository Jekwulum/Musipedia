import json

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
        # pprint(data[3]['artist_albums'])
        for artist in data:
            if artist['full_name'] == str(self.artist1.full_name):
                self.assertEqual(artist['artist_albums'][0]['title'], str(self.album1.title))

    def test_create_artist(self):
        data = {
            "full_name": "Christian Blur",
            "record_label": "Quebec Int",
            "stage_name": "Chris-o",
            "dob": "2003-09-10",
            "albums": [
                {"title": "album 7"},
                {"title": "album 9"}
            ],
            "songs": [{"title": "song 2"}]
        }
        response = self.client.post(
            APITestUtils.get_artists_url(),
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        data = response.data
        print("data: ")
        pprint(data)
        self.assertEqual(data['full_name'], "Christian Blur")
        self.assertIn('artist_albums', data)
        self.assertIn('title', data['artist_albums'][0])

    def test_artist_update(self):
        data = {
            "full_name": "Christian Blur",
            "stage_name": "Chris-2",
            "dob": "2003-09-10",
            "record_label": "Quebec Int",
            "albums": [
                {
                    "title": "album 10"
                }
            ],
            "songs": [
                {
                    "title": "song 10"
                }
            ]
        }

        response = self.client.patch(
            APITestUtils.get_artist_details_url(self.artist1.stage_name),
            data=data,
            format='json'
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_artist(self):
        response = self.client.delete(
            APITestUtils.get_artist_details_url(self.artist1.stage_name)
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data['message'], 'Deleted')
