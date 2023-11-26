from django.contrib import admin

from communities.models import (
    Community,
    CommunityMembership,
    CommunityPost,
    CommunityPostComment,
)


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    pass


@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    pass


@admin.register(CommunityPostComment)
class CommunityPostCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(CommunityMembership)
class CommunityMembershipAdmin(admin.ModelAdmin):
    pass
