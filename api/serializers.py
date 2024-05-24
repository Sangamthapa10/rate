from rest_framework import serializers
from . import models

class ImageModelSerializers(serializers.ModelSerializer):
    class Meta:
        model=models.mode
        fields='__all__'