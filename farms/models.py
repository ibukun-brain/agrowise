import uuid

import auto_prefetch
from django.conf import settings
from django.db import models

from agrowise.utils.choices import CropTypes, SoilTypes
from agrowise.utils.media import MediaHelper
from agrowise.utils.models import TimeBasedModel
from farms.fields import OrderField


class Farm(TimeBasedModel):
    owner = auto_prefetch.ForeignKey("home.CustomUser", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    address = models.CharField(max_length=200)
    farm_phone_number = models.CharField(max_length=11, blank=True)
    farm_email = models.EmailField(unique=True, blank=True)
    farm_website = models.CharField(max_length=11, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name", "-created_at"]
        indexes = [
            models.Index(fields=["name", "-created_at"])
        ]


class Field(TimeBasedModel):
    uid = models.UUIDField(default=uuid.uuid4, primary_key=False, editable=False)
    farm = auto_prefetch.ForeignKey("farms.Farm", on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    size = models.PositiveBigIntegerField(blank=True)
    crop_type = models.CharField(max_length=50, choices=CropTypes.choices, blank=True)
    soil_type = models.CharField(max_length=50, choices=SoilTypes.choices, blank=True)

    def __str__(self):
        return self.uid


class Crop(TimeBasedModel):
    farm = auto_prefetch.ForeignKey("farms.Farm", on_delete=models.CASCADE)
    field = auto_prefetch.ForeignKey(
        "farms.Field",
        on_delete=models.CASCADE,
        blank=True,
    )
    slug = models.SlugField(unique=True, blank=True)
    planting_date = models.DateField(null=True, blank=True)
    harvest_date = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=200)
    image = models.ImageField(blank=True, upload_to=MediaHelper.get_image_upload_path)
    pest_susceptiblity = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return f"http://localhost:8000/{settings.STATIC_URL}/image/placeholder.jpg"


class CropImages(TimeBasedModel):
    text = models.CharField(max_length=100, blank=True)
    crop = auto_prefetch.ForeignKey("farms.Crop", on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to=MediaHelper.get_image_upload_path)
    order = OrderField(blank=True, for_fields=["crop"], help_text="Image order number")

    class Meta:
        verbose_name_plural = "Crop Images"

    def __str__(self):
        return self.order


class ProduceListing(TimeBasedModel):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=False)
    owner = auto_prefetch.ForeignKey(
        "home.CustomUser",
        on_delete=models.CASCADE
    )
    farm = auto_prefetch.ForeignKey(
        "farms.Farm",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    crops = models.ForeignKey(
        "farms.Crop",
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    price = models.PositiveBigIntegerField()
    availability = models.PositiveSmallIntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(
        upload_to=MediaHelper.get_image_upload_path, blank=True
    )

    class Meta:
        ordering = ["name", "-created_at"]
        indexes = [
            models.Index(fields=["name", "-created_at"])
        ]

    def __str__(self):
        return self.uid

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return f"http://localhost:8000/{settings.STATIC_URL}/image/placeholder.jpg"
