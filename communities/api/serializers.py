from django.db.utils import IntegrityError
from rest_framework import serializers

from communities.models import (
    Community,
    CommunityMembership,
    CommunityPost,
    CommunityPostComment,
)


class CommunitySerializer(serializers.ModelSerializer):
    admin = serializers.StringRelatedField(many=False)
    members = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Community
        fields = [
            "name",
            "admin",
            "slug",
            "about",
            "members",
            "created_at",
        ]
   
    def create(self, validated_data):
        return Community.object.create(**validated_data)

    def create(self, validated_data):
        return Community.objects.create(**validated_data)

    def to_representation(self, instance):
        request = self.context["request"]
        current_user = request.user
        members = instance.members.all()
        data = super().to_representation(instance)
        data.update(
            {
                "has_joined": False,
            }
        )
        if current_user in members:
            data.update(
                {
                    "has_joined": True,
                }
            )
        return data


class CommunityMembershipSerializer(serializers.ModelSerializer):
    member = serializers.StringRelatedField()
    community = serializers.StringRelatedField()

    class Meta:
        model = CommunityMembership
        fields = [
            "uid",
            "member",
            "community",
            "date_joined",
        ]
        extra_kwargs = {
            "uid": {"read_only": True},
        }

    def create(self, validated_data):
        try:
            return CommunityMembership.objects.create(**validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError(
                {
                    "detail": "You are a member of this community",
                },
            ) from e

    def update(self, instance, validated_data):
        community = instance.community
        community.members.remove(instance.member)
        return instance


class CommunityPostSerializer(serializers.ModelSerializer):
    community = serializers.StringRelatedField(many=False, read_only=True)
    owner = serializers.StringRelatedField(many=False)

    class Meta:
        model = CommunityPost
        fields = [
            "uid",
            "community",
            "post",
            "owner",
            "created_at",
        ]
        extra_kwargs = {
            "uid": {
                "read_only": True,
            }
        }

    def create(self, validated_data):
        owner = validated_data.get("owner", None)
        community = validated_data.get("community", None)
        if owner not in community.members.all():
            raise serializers.ValidationError(
                {"detail": "You must be a member of this community"}
            )
        return CommunityPost.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.post = validated_data.get("post")
        instance.save()
        return instance


class CommunityCommentSerializer(serializers.ModelSerializer):
    community_post = CommunityPostSerializer(many=False, read_only=True)
    # community_post = serializers.HiddenField(
    #     default=CommunityPostSerializer
    # )
    user = serializers.StringRelatedField()

    class Meta:
        model = CommunityPostComment
        fields = [
            "community_post",
            "user",
            "text",
            "created_at",
        ]

    def create(self, validated_data):
        return CommunityPostComment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.text = validated_data.get("text")
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = CommunityPostComment
        fields = [
            "uid",
            "user",
            "text",
            "created_at",
        ]


class CommunityPostCommentSerializer(serializers.ModelSerializer):
    community = serializers.StringRelatedField(many=False, read_only=True)
    owner = serializers.StringRelatedField(many=False)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = CommunityPost
        fields = ["uid", "community", "post", "owner", "created_at", "comments"]
