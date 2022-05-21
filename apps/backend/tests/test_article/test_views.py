import json

import pytest
from django.contrib.auth import get_user_model

from articles.models import Article

User = get_user_model()


@pytest.mark.django_db
class TestArticle:
    def test_get_news(self, api_client):
        Article.objects.create(
            title='title',
            title_trans='title_trans',
            article=1,
            preview='preview',
            author=User.objects.create(username='test_user_for_article'),
            body='body',
            short_summary='short_summary',
            views=0
        )

        response = api_client().get("/api/v1/articles/articles")
        articles = response.data

        assert response.status_code == 200
        for article in articles:
            assert "title" in article
            assert "preview" in article
            assert "short_summary" in article
            assert "views" in article
            assert "rating" in article

