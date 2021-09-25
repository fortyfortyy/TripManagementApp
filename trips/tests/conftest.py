import pytest

from trips.models import Country, City, Days, Description, Tag, Trip, TripPlan


@pytest.fixture
def trip_plan_create():
    return TripPlan.objects.create(
        owner='fake_owner',
        name='fake_name',
        is_private=True,
    )


@pytest.fixture
def trip_create():
    return Trip.objects.create(
        plan='fake_trip_plan',
        name='fake_name',
        short_description='fake_description',
        countries='fake_country',
        cities='fake_city',
    )


@pytest.fixture
def country_create():
    return Country.objects.create(
        country='fake_country',
    )


@pytest.fixture
def city_create():
    return City.objects.create(
        city='fake_city',
    )


@pytest.fixture
def description_create():
    return Description.objects.create(
        trip='fake_trip',
        content='fake_description',
    )


@pytest.fixture
def days_create():
    return Days.objects.create(
        trip='fake_trip',
        day_from='2021-01-10',
        day_to='2021-11-10',
    )


@pytest.fixture
def tag_create():
    return Tag.objects.create(
        name='fake_tag',
    )
