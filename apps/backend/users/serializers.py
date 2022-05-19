from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email']

    def save(self, **kwargs):
        user = super().save(**kwargs)
        user.set_password(self.validated_data['password'])
        user.save()
        return user
