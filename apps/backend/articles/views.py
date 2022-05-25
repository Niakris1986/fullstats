from django.db.models import Count, F, Q
from rest_framework import permissions
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView

from articles.models import Article, LikeChoices, LikeArticle
from articles.serializers import ArticleListPreviewSerializer, ArticleDetailSerializer, \
    LikeArticleCreateUpdateSerializer
from utils.pagination_classes import ArticlePagination


class ArticleListAPIView(ListAPIView):
    serializer_class = ArticleListPreviewSerializer
    pagination_class = ArticlePagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['rating', 'publish']

    def get_queryset(self):
        queryset = Article.objects.all().annotate(
            plus=Count('likes', filter=Q(likes__rating=LikeChoices.POSITIVE.value)),
            neg=Count('likes', filter=Q(likes__rating=LikeChoices.NEGATIVE.value))
        ).annotate(rating=F('plus') - F('neg'))

        return queryset


class ArticleRetrieveAPIView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer

    def get_queryset(self):
        queryset = Article.objects.all().annotate(
            plus=Count('likes', filter=Q(likes__rating=LikeChoices.POSITIVE.value)),
            neg=Count('likes', filter=Q(likes__rating=LikeChoices.NEGATIVE.value))
        ).annotate(rating=F('plus') - F('neg'))
        return queryset


class LikeCreateDeleteArticleAPIView(CreateAPIView, RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = LikeArticle.objects.all()
    serializer_class = LikeArticleCreateUpdateSerializer
    partial = True

    def perform_create(self, serializer):
        serializer.save(article_id=self.kwargs['pk'], user=self.request.user)

    def get_object(self):
        return LikeArticle.objects.get(pk=self.kwargs['pk'], user=self.request.user)
