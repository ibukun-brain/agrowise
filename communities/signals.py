import uuid

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify

from communities.models import Community, CommunityMembership, CommunityPost


def create_slug(model, instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = model.objects.filter(slug=slug).order_by("pk")
    exists = qs.exists()
    if exists:
        uuid_start = str(uuid.uuid1()).split("-", 1)[0]
        new_slug = "%s-%s" % (slug, uuid_start)
        return create_slug(model, instance, new_slug=new_slug)

    return slug


@receiver(pre_save, sender=Community)
def pre_save_community_slug_reciever(sender, instance, **kwargs):
    community = Community()
    if not instance.slug:
        instance.slug = create_slug(Community, instance)
    try:
        community = Community.objects.get(pk=instance.pk)
    except Community.DoesNotExist:
        pass
    if instance.name != community.name:
        instance.slug = create_slug(Community, instance)


@receiver(post_save, sender=Community)
def post_save_add_admin_to_community_membership(sender, instance, created, **kwargs):
    if created:
        CommunityMembership.objects.create(
            community=instance, member=instance.admin, date_joined=timezone.now()
        )


@receiver(pre_save, sender=CommunityPost)
def pre_save_community_post_slug_reciever(sender, instance, **kwargs):
    community_post = CommunityPost()
    if not instance.slug:
        instance.slug = create_slug(CommunityPost, instance)
    try:
        community_post = CommunityPost.objects.get(pk=instance.pk)
    except CommunityPost.DoesNotExist:
        pass
    if instance.name != community_post.name:
        instance.slug = create_slug(Community, instance)
