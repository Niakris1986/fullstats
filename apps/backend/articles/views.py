from rest_framework.views import APIView, Response

from articles.models import Article
from articles.serializers import ArticleListPreviewSerializer


class ArticleListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Article.objects.all()
        serializer = ArticleListPreviewSerializer(queryset, many=True)
        return Response(serializer.data, status=200)