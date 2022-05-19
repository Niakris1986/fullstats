from rest_framework.views import APIView, Response

from users.serializers import UserCreateSerializer


class UserCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=201)
