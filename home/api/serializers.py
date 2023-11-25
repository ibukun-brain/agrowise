from django.conf import settings
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreatePasswordRetypeSerializer, UserSerializer
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from agrowise.utils.urls import get_url
from home.models import CustomUser

User = get_user_model()


class CustomUserCreatePasswordRetypeSerializer(UserCreatePasswordRetypeSerializer):
    full_name = serializers.CharField(max_length=200)

    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = [
            "full_name",
            "first_name",
            "last_name",
            # "date_of_birth",
            "email",
            # "mobile_no",
            # "gender",
            "password",
        ]
        extra_kwargs = {
            "first_name": {
                "read_only": True,
            },
            "last_name": {
                "read_only": True,
            },
        }

    def create(self, validated_data):
        full_name = validated_data.pop("full_name")
        first_name = full_name.split(" ")[0]
        last_name = ""
        try:
            last_name = full_name.split(" ")[1]
        except IndexError:
            last_name = ""
        validated_data.update(
            {
                "first_name": first_name,
                "last_name": last_name,
            }
        )
        return super().create(validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        _ = data.pop("full_name")
        return data


class CustomUserSerializer(UserSerializer):
    image_url = serializers.SerializerMethodField("_image_url")

    @extend_schema_field(OpenApiTypes.URI)
    def _image_url(self, obj):
        request = self.context["request"]
        url = get_url(request, path_str=None, default=settings.STATIC_URL)
        if obj.profile_pic:
            return obj.profile_pic.url

        return f"{url}image/placeholder.jpg"

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
