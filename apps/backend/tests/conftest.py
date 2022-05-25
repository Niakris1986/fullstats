import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from tests.test_article.fixtures import create_article
from tests.test_user.fixtures import generate_username


@pytest.fixture
def api_client():
    return APIClient


@pytest.fixture
def new_user():
    User = get_user_model()
    return User.objects.create(username=generate_username())


@pytest.fixture
def new_article():
    return create_article()


@pytest.fixture
def api_auth_client(api_client, new_user):
    client = api_client()
    client.force_login(user=new_user)
    return client
