from rest_framework.views import APIView, Response
from rest_framework.pagination import PageNumberPagination

from articles.models import Article
from articles.serializers import ArticleListPreviewSerializer


class ArticleListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Article.objects.all()
        pg = PageNumberPagination()
        pg.page_size_query_param = "page_size"
        queryset = pg.paginate_queryset(queryset, request)
        serializer = ArticleListPreviewSerializer(queryset, many=True)
        return Response(serializer.data, status=200)
