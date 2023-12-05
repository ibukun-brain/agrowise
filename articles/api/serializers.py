from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from articles.models import Article, Category, Comment

# from drf_spectacular.types import OpenApiTypes


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "name",
            "slug",
        ]


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Article Success Response Example",
            summary="Success Response",
            value={
                "author": "ibukunolaifa1984@gmail.com",
                "category": "Guides",
                "image": "/media/images/article/2023-11-26/image.jpg",
                "name": "Women in Farming",
                "slug": "women-in-farming",
                "status": "published",
                "text": "<p>sdasdas</p>",
                "comment_count": 1,
                "created_at": "2023-11-26T17:12:47.615164+01:00",
            },
            # request_only=True, # signal that example only applies to requests
            # response_only=True, # signal that example only applies to responses
            status_codes=[200],
        ),
        OpenApiExample(
            "Article Bad Request Response Example",
            summary="Error Response",
            # description='longer description',
            value={
                "error": "Bad Request",
            },
            status_codes=[400],
        ),
    ],
)
class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False, read_only=False)
    category = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Article
        fields = [
            "author",
            "category",
            "image",
            "name",
            "slug",
            "status",
            "text",
            "comment_count",
            "created_at",
        ]


class UserCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = [
            "user",
            "text",
            "created_at",
        ]


class UserArticleCommentSerializer(serializers.ModelSerializer):
    article = serializers.StringRelatedField(many=False)
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = Comment
        fields = [
            "article",
            "user",
            "text",
            "created_at",
        ]


class ArticleCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False)
    comments = UserCommentSerializer(many=True, read_only=False)
    category = serializers.StringRelatedField(many=False)

    class Meta:
        model = Article
        fields = [
            "author",
            "category",
            "name",
            "slug",
            "comments",
            "comment_count",
        ]
