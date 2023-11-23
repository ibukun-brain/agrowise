from django.contrib import admin

from farms.models import Crop, CropImages, Farm, Field, ProduceListing


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    pass


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    pass


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    pass


@admin.register(CropImages)
class CropImagesAdmin(admin.ModelAdmin):
    pass


@admin.register(ProduceListing)
class ProduceListingAdmin(admin.ModelAdmin):
    pass
