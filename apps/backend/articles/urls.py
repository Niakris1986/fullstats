from django.urls import path

from articles.views import ArticleListAPIView, ArticleRetrieveAPIView, LikeCreateDeleteArticleAPIView

urlpatterns = [
    path('articles', ArticleListAPIView.as_view(), name='articles-list'),
    path('articles/<int:pk>', ArticleRetrieveAPIView.as_view(), name='articles-detail'),
    path('articles/<int:pk>/like', LikeCreateDeleteArticleAPIView.as_view(), name='articles-like'),
]

