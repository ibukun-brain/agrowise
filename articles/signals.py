import uuid

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from articles.models import Article


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


@receiver(pre_save, sender=Article)
def pre_save_article_slug_reciever(sender, instance, **kwargs):
    article = Article()
    if not instance.slug:
        instance.slug = create_slug(Article, instance)
    try:
        article = Article.objects.get(pk=instance.pk)
    except Article.DoesNotExist:
        pass
    if instance.name != article.name:
        instance.slug = create_slug(Article, instance)
