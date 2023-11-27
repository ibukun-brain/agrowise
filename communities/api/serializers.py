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
                    "error": "You are a member of this community",
                },
                code=400,
            ) from e


class CommunityPostSerializer(serializers.ModelSerializer):
    community = CommunitySerializer(many=False, read_only=True)
    owner = serializers.StringRelatedField(many=False)

    class Meta:
        model = CommunityPost
        fields = [
            "uid",
            "community",
            "name",
            "slug",
            "owner",
            "created_at",
        ]


class CommunityCommentSerializer(serializers.Serializer):
    community_post = CommunityPostSerializer(many=False, read_only=True)
    member = serializers.StringRelatedField()

    class Meta:
        model = CommunityPostComment
        fields = [
            "community_post",
            "member",
            "text",
            "created_at",
        ]
