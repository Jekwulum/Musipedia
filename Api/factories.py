import factory
import factory.fuzzy
import datetime

from Api.models import (Artist, Album)


class ArtistFactory(factory.django.DjangoModelFactory):
    full_name = factory.fuzzy.FuzzyText(length=15)
    stage_name = factory.fuzzy.FuzzyText(length=15)
    record_label = factory.fuzzy.FuzzyText(length=15)
    dob = factory.fuzzy.FuzzyDate(datetime.date(2010, 1, 1))
    dod = factory.fuzzy.FuzzyDate(datetime.date(2010, 1, 1))

    class Meta:
        model = Artist


class AlbumFactory(factory.django.DjangoModelFactory):
    title = factory.fuzzy.FuzzyText(length=25)
    artist = factory.SubFactory(ArtistFactory)

    class Meta:
        model = Album
