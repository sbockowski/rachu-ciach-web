import pytest
from rest_framework.test import APIClient
from tests.factories import UserFactory

@pytest.fixture
def user(db):
    return UserFactory()

@pytest.fixture
def other_user(db):
    return UserFactory()

@pytest.fixture
def api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def anon_client():
    return APIClient()