import json

import pytest
import random
from django.contrib.auth import get_user_model

from articles.models import Article

User = get_user_model()


@pytest.mark.django_db
class TestArticle:
    def test_get_news(self, api_client):
        self.create_article()

        response = api_client().get("/api/v1/articles/articles")
        articles = response.data

        assert response.status_code == 200
        for article in articles:
            assert "title" in article
            assert "preview" in article
            assert "short_summary" in article
            assert "views" in article
            assert "rating" in article

    def create_article(self):

        Article.objects.create(
            title='title',
            title_trans='title_trans',
            article=1,
            preview='preview',
            author=User.objects.create(username=f'user {random.randint(0, 9999)}'),
            body='body',
            short_summary='short_summary',
            views=0
        )

    def test_pagination_news(self, api_client):
        page_size = 2
        for _ in range(page_size * 3):
            self.create_article()
        response = api_client().get(f"/api/v1/articles/articles?page_size={page_size}")
        response2 = api_client().get(f"/api/v1/articles/articles?page_size={page_size}&page=2")
        articles = response.data
        assert response.status_code == 200
        assert len(articles) == page_size
        assert response2.data != response.data
        assert list([x["id"] for x in response.data]) != list([x["id"] for x in response2.data])