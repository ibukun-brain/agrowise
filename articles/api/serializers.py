from rest_framework import serializers

from articles.models import Article, Category, Comment

# from drf_spectacular.utils import extend_schema_field
# from drf_spectacular.types import OpenApiTypes



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "name",
            "slug",
        ]


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
