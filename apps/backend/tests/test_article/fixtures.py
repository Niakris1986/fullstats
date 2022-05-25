import random

from faker import Faker

from articles.models import Article
from django.contrib.auth import get_user_model
from tests.test_user.fixtures import generate_username


def create_article() -> Article:
    faker = Faker()
    return Article.objects.create(
        title=faker.word(),
        title_trans=faker.word(),
        article=random.randint(1, 10),
        preview=faker.sentences(),
        author=get_user_model().objects.create(username=generate_username()),
        body=faker.text(),
        short_summary=faker.text()[:50],
        views=0
    )
