from django.contrib.auth import get_user_model
from djoser.serializers import UserCreatePasswordRetypeSerializer, UserSerializer
from rest_framework import serializers

from home.models import CustomUser

User = get_user_model()


class CustomUserCreatePasswordRetypeSerializer(UserCreatePasswordRetypeSerializer):
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "email",
            "mobile_no",
            "gender",
            "password",
        ]


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            # "username",
            "profile_pic",
            "image_url",
            "email",
            "mobile_no",
        )
        extra_kwargs = {
            "first_name": {
                "read_only": True,
            },
            "last_name": {
                "read_only": True,
            },
            "email": {
                "read_only": True,
            },
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        _ = data.pop("profile_pic")
        return data


class OpenAPISerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=250)


class WeatherForecastSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=200)
