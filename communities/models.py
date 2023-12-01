import uuid

import auto_prefetch
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import truncatechars

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
    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, related_name="community_post"
    )
    post = models.TextField()
    owner = models.ForeignKey(
        "home.CustomUser", on_delete=models.CASCADE, related_name="community_post"
    )

    @property
    def trunc_post(self):
        return truncatechars(self.post, 50)

    def __str__(self):
        return self.trunc_post

    def clean(self):
        # To assign exceptions to a specific field instantiate the ValidationError
        # with a dictionary, where the keys are the field names.
        if self.owner not in self.community.members.all():
            raise ValidationError(
                {"owner": ("You must be a member of this community")}
                # {'name': ('invalid name')} for errors multiple fields
            )


class CommunityPostComment(TimeBasedModel):
    uid = models.UUIDField(default=uuid.uuid4)
    community_post = auto_prefetch.ForeignKey(
        CommunityPost, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey("home.CustomUser", on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"{self.user}"

    class Meta:
        ordering = ("-created_at",)
        indexes = [models.Index(fields=["-created_at"])]
