from rest_framework import serializers
from . import models
from .models import Type,mode
class ImageModelSerializers(serializers.ModelSerializer):
    class Meta:
        model=models.mode
        fields='__all__'




class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name']
class categorySerializer(serializers.ModelSerializer):
    category = CategorySerializers(read_only=True)

    class Meta:
        model = Type
        fields = ['id', 'name', 'default', 'status', 'dp', 'description', 'category']






class ModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = mode
        fields = ['id', 'name', 'img', 'score', 'type', 'status']

class TypeSerializer(serializers.ModelSerializer):
    modes = ModeSerializer(many=True, required=False)  # Nested serializer for related modes

    class Meta:
        model = Type
        fields = ['id', 'name', 'default', 'status', 'dp', 'description', 'modes','category']

    def create(self, validated_data):
        modes_data = validated_data.pop('modes', [])  # Extract modes data from validated_data
        type_instance = Type.objects.create(**validated_data)  # Create Type instance

        # Create Mode instances related to the Type
        for mode_data in modes_data:
            mode.objects.create(type=type_instance, **mode_data)
        return type_instance

    def update(self, instance, validated_data):
        modes_data = validated_data.pop('modes', [])  # Extract modes data from validated_data

        # Update Type instance fields
        instance.name = validated_data.get('name', instance.name)
        instance.default = validated_data.get('default', instance.default)
        instance.status = validated_data.get('status', instance.status)
        instance.dp = validated_data.get('dp', instance.dp)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # Update or create related Mode instances
        for mode_data in modes_data:
            mode_id = mode_data.get('id')
            if mode_id:
                mode_instance = mode.objects.get(id=mode_id, type=instance)
                mode_serializer = ModeSerializer(mode_instance, data=mode_data)
            else:
                mode_serializer = ModeSerializer(data=mode_data)
            if mode_serializer.is_valid():
                mode_serializer.save(type=instance)
        return instance