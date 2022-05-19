import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUser:
    def test_register_new_user(self, api_client):
        test_json = {
            'username': 'test_user',
            'password': 'superstrong_password123',
            'email': 'test@mail.ru'
        }

        response = api_client().post("/api/v1/users/users", data=test_json, format='json')
        user = User.objects.filter(username='test_user').first()

        assert response.status_code == 201
        assert user is not None
        assert user.email == 'test@mail.ru'
        assert user.check_password('superstrong_password123')
