import uuid

import auto_prefetch
from django.db import models

from agrowise.utils.models import NamedTimeBasedModel, TimeBasedModel


class Community(NamedTimeBasedModel):
    admin = auto_prefetch.ForeignKey(
        "home.CustomUser", on_delete=models.CASCADE, related_name="community_admin"
    )
    slug = models.SlugField(unique=True, blank=True)
    about = models.TextField(max_length=200)
    members = models.ManyToManyField("home.CustomUser", through="CommunityMembership")

    class Meta:
        ordering = ["name", "-created_at"]
        indexes = [models.Index(fields=["name", "-created_at"])]
        verbose_name_plural = "Communities"

    def __str__(self):
        return self.name


class CommunityMembership(TimeBasedModel):
    uid = models.UUIDField(default=uuid.uuid4)
    member = auto_prefetch.ForeignKey(
        "home.CustomUser",
        on_delete=models.CASCADE,
    )
    community = auto_prefetch.ForeignKey(Community, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_members",
                fields=["member", "community"],
            )
        ]

    def __str__(self):
        return str(self.date_joined)


class CommunityPost(TimeBasedModel):
    uid = models.UUIDField(default=uuid.uuid4)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    owner = models.ForeignKey("home.CustomUser", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CommunityPostComment(TimeBasedModel):
    uid = models.UUIDField(default=uuid.uuid4)
    community_post = auto_prefetch.ForeignKey(
        CommunityPost,
        on_delete=models.CASCADE,
        # null=True,
        # blank=True
    )
    member = models.ForeignKey("home.CustomUser", on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"{self.member} ----> {self.community_post.name}"
