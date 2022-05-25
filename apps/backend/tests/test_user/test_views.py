import pytest
from django.contrib.auth import get_user_model
from faker import Faker

User = get_user_model()


@pytest.mark.django_db
class TestUser:
    def test_register_new_user(self, api_client):
        faker = Faker()
        profile = faker.profile()
        test_json = {
            'username': profile['username'],
            'password': profile['ssn'],
            'email': profile['mail']
        }

        print(test_json)
        response = api_client().post("/api/v1/users/users", data=test_json, format='json')
        user = User.objects.filter(username=profile['username']).first()

        assert response.status_code == 201
        assert user is not None
        assert user.email == profile['mail']
        assert user.check_password(profile['ssn'])