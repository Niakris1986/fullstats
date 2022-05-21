from typing import Iterable

from rest_framework import serializers

from articles.models import Article, LikeArticle


class ArticleListPreviewSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj: Article):
        ratings: Iterable[LikeArticle] = obj.likes.all()
        result = 0
        for rating in ratings:
            result += rating.rating
        return result

    class Meta:
        model = Article
        fields = ['id', 'title', 'preview', 'short_summary', 'views', 'rating']
