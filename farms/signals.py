import uuid

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from farms.models import Crop, Farm


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


@receiver(pre_save, sender=Farm)
def pre_save_farm_slug_reciever(sender, instance, **kwargs):
    farm = Farm()
    if not instance.slug:
        instance.slug = create_slug(Farm, instance)
    try:
        farm = Farm.objects.get(pk=instance.pk)
    except Farm.DoesNotExist:
        pass
    if instance.name != farm.name:
        instance.slug = create_slug(Farm, instance)


@receiver(pre_save, sender=Crop)
def pre_save_crop_slug_reciever(sender, instance, **kwargs):
    crop = Crop()
    if not instance.slug:
        instance.slug = create_slug(Crop, instance)
    try:
        crop = Crop.objects.get(pk=instance.pk)
    except Crop.DoesNotExist:
        pass
    if instance.name != crop.name:
        instance.slug = create_slug(Crop, instance)
