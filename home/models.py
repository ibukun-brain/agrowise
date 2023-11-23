import uuid

import auto_prefetch
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField

from agrowise.utils.choices import Gender
from agrowise.utils.managers import CustomUserManager
from agrowise.utils.media import MediaHelper
from agrowise.utils.models import TimeBasedModel
from agrowise.utils.validators import FileValidatorHelper


class CustomUser(TimeBasedModel, AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    # username = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    uid = models.UUIDField(default=uuid.uuid4)
    email = models.EmailField(verbose_name="email address", unique=True)
    mobile_no = models.CharField(
        max_length=11,
        blank=True,
        validators=[MinLengthValidator(11)],
    )
    date_joined = models.DateTimeField(default=timezone.now)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=15, choices=Gender.choices, blank=True)
    profile_pic = ResizedImageField(
        upload_to=MediaHelper.get_image_upload_path,
        blank=True,
        verbose_name="Profile Picture",
        validators=[
            FileValidatorHelper.validate_file_size,
            FileValidatorHelper.validate_image_extension,
        ],
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()

    class Meta(auto_prefetch.Model.Meta):
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["date_joined"]
        indexes = [models.Index(fields=["date_joined"])]

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    @property
    def image_url(self):

        if self.profile_pic:
            return self.profile_pic.url

        return f"http://localhost:8000{settings.STATIC_URL}avatar/placeholder.jpg"
