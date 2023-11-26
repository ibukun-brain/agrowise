from rest_framework import serializers

from articles.models import Article, Category, Comment


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
            "name",
            "slug",
            "status",
            "content",
            "comment_count",
        ]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = [
            "user",
            "text",
            "created_at",
        ]


class ArticleCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False)
    comments = CommentSerializer(many=True, read_only=False)

    class Meta:
        model = Article
        fields = [
            "author",
            "name",
            "slug",
            "comments",
        ]
