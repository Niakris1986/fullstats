from django.urls import path

from users.views import UserCreateAPIView

urlpatterns = [
    path('users', UserCreateAPIView.as_view(), name='users-create')
]
