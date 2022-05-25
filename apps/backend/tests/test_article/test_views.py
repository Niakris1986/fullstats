import pprint
import random

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from articles.models import LikeArticle, LikeChoices
from tests.test_article.fixtures import create_article

User = get_user_model()


@pytest.mark.django_db
class TestListArticle:
    url = reverse('articles-list')

    def test_get_news(self, api_client):
        create_article()
        response = api_client().get(self.url)
        articles = response.data
        assert response.status_code == 200
        for article in articles['results']:
            assert "title" in article
            assert "preview" in article
            assert "short_summary" in article
            assert "views" in article
            assert "rating" in article

    def test_pagination_news(self, api_client):
        page_size = random.randint(1, 10)
        for _ in range(page_size * 3):
            create_article()
        response = api_client().get(f"{self.url}?page_size={page_size}")
        response2 = api_client().get(f"{self.url}?page_size={page_size}&page=2")
        articles = response.data['results']
        assert response.status_code == 200
        assert len(articles) == page_size
        assert response2.data != response.data
        assert list([x["id"] for x in response.data['results']]) != list([x["id"] for x in response2.data['results']])

    def test_ordering_news_by_publish(self, api_client):
        page_size = 3
        articles = []
        for _ in range(page_size):
            articles.append(create_article())
        response = api_client().get(f"{self.url}?page_size={page_size}&ordering=publish")
        response2 = api_client().get(f"{self.url}?page_size={page_size}&ordering=-publish")
        assert response.status_code == 200
        assert response2.status_code == 200
        assert [x['id'] for x in response2.data['results']] == [x['id'] for x in response.data['results']][::-1]

    def test_ordering_news_by_rating(self, api_client, new_user):
        page_size = 3
        articles = []
        for _ in range(page_size):
            articles.append(create_article())
        target_article = articles[random.randint(0, 2)]
        LikeArticle.objects.create(article=target_article, user=new_user, rating=LikeChoices.POSITIVE)
        response = api_client().get(f"{self.url}?page_size={page_size}&ordering=rating")
        response2 = api_client().get(f"{self.url}?page_size={page_size}&ordering=-rating")
        assert response.status_code == 200
        assert response2.status_code == 200
        pprint.pprint(response.data['results'])
        pprint.pprint(response2.data['results'])
        assert target_article.id == response.data['results'][2]['id']
        assert target_article.id == response2.data['results'][0]['id']


@pytest.mark.django_db
class TestDetailArticle:

    def test_retrieve_one_article(self, api_client, new_article):
        url = '/api/v1/articles/articles/' + str(new_article.id)
        res = api_client().get(url)
        article = res.data
        assert "title" in article
        assert "preview" in article
        assert "body" in article
        assert "views" in article
        assert "rating" in article

    def test_create_like_article(self, api_auth_client, new_article):
        url = '/api/v1/articles/articles/' + str(new_article.id) + '/like'
        res = api_auth_client.post(url, format='json', data={'rating': 1})
        new_article.refresh_from_db()
        assert res.status_code == 201
        assert new_article.likes.all().count() == 1
        assert new_article.likes.first().rating == 1

    def test_update_like_article(self, api_auth_client, new_article):
        url = '/api/v1/articles/articles/' + str(new_article.id) + '/like'
        res = api_auth_client.post(url, format='json', data={'rating': 1})
        new_article.refresh_from_db()
        assert res.status_code == 201
        assert new_article.likes.all().count() == 1
        assert new_article.likes.first().rating == 1
        res = api_auth_client.patch(url, format='json', data={'rating': -1})
        assert res.status_code == 200
        assert new_article.likes.all().count() == 1
        assert new_article.likes.first().rating == -1

    def test_delete_like_article(self, api_auth_client, new_article):
        url = '/api/v1/articles/articles/' + str(new_article.id) + '/like'
        res = api_auth_client.post(url, format='json', data={'rating': 1})
        new_article.refresh_from_db()
        assert res.status_code == 201
        assert new_article.likes.all().count() == 1
        assert new_article.likes.first().rating == 1
        res = api_auth_client.delete(url, format='json', data={'rating': 1})
        new_article.refresh_from_db()
        assert res.status_code == 204
        assert new_article.likes.all().count() == 0
