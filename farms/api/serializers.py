from rest_framework import serializers

from farms.models import Crop, CropImages, Farm, Field, ProduceListing


class FarmSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = Farm
        fields = [
            "owner",
            "name",
            "slug",
            "address",
            "farm_phone_number",
            "farm_email",
            "farm_website"
        ]


class FieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Field
        fields = "__all__"


class CropSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crop
        fields = "__all__"


class CropImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CropImages
        fields = "__all__"


class ProduceListingSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = ProduceListing
        fields = [
            "owner",
            "uid",
            "name",
            "type",
            "availability",
            "price",
            "description",
            "created_at",
        ]
