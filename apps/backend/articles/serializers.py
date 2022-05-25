from rest_framework import serializers

from articles.models import Article, LikeArticle


class ArticleListPreviewSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'preview', 'short_summary', 'views', 'rating']


class ArticleDetailSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'preview', 'body', 'views', 'rating']


class LikeArticleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeArticle
        fields = ['rating']
