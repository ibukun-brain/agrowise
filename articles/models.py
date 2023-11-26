import auto_prefetch
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from agrowise.utils.choices import ArticleChoices
from agrowise.utils.media import MediaHelper
from agrowise.utils.models import NamedTimeBasedModel, TimeBasedModel, CategoryModel
from django.template.defaultfilters import striptags, safe, escape

class Category(CategoryModel):
    pass


class Article(NamedTimeBasedModel):
    slug = models.SlugField(unique=True, blank=True)
    author = auto_prefetch.ForeignKey(
        "home.CustomUser",
        on_delete=models.CASCADE
    )
    category = auto_prefetch.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to=MediaHelper.get_image_upload_path,
    )
    status = models.CharField(
        choices=ArticleChoices.choices,
        default=ArticleChoices.Draft,
        max_length=50,
    )
    text = RichTextUploadingField()

    def __str__(self):
        return self.name

    @property
    def content(self):
        text = self.text
        return text

    @property
    def comment_count(self):
        # comment = Comment.objects.select_related("article", "user") \
        #         .filter(article=self).count()
        comment = self.comments.count()
        return comment


class Comment(TimeBasedModel):
    article = auto_prefetch.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    user = auto_prefetch.ForeignKey(
        "home.CustomUser",
        on_delete=models.CASCADE,
    )
    text = models.TextField()

    def __str__(self):
        return f"{self.user} ---> {self.created_at}"