from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import mode, session, Type, Category
from . import serializers
import random
from django.db.models import Count, F


# class Create(APIView):


class ImageView(APIView):

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if id  == 0:
            count = mode.objects.count()
            if count < 2:
                return Response({'error': 'Not enough images available'}, status=status.HTTP_400_BAD_REQUEST)
            random_indices = random.sample(range(count), 2)
            images = [mode.objects.all( )[index] for index in random_indices]
            serializer = serializers.ImageModelSerializers(images, context={"request": request}, many=True)
            top=mode.objects.order_by('-score')[:5]
            serializerq = serializers.ImageModelSerializers(top, context={"request": request}, many=True)
            category=Type.objects.all();
            category_serializer=serializers.categorySerializer(category,context={"request": request}, many=True)
            data={
                'a':serializer.data,
                'b':serializerq.data,
                'c':category_serializer.data
            }


            return Response(data)
        else:
            count = mode.objects.filter(type=id).count()
            print(count)
            if count < 2:
                return Response({'error': 'Not enough images available'}, status=status.HTTP_400_BAD_REQUEST)
            random_indices = random.sample(range(count), 2)
            images_queryset = mode.objects.filter(type=id)

            images = [mode.objects.filter(type=id)[index] for index in random_indices]
            print(images)
            serializer = serializers.ImageModelSerializers(images, context={"request": request}, many=True)

            top = mode.objects.filter(type=id).order_by('-score')[:5]
            serializer_top = serializers.ImageModelSerializers(top, context={"request": request}, many=True)

            data = {
                'a': serializer.data,
                'b': serializer_top.data,
            }

            return Response(data)



    def post(self, request, *args, **kwargs):
        exclude = request.data.get("ids", [])
        selected = request.data.get("selected")
        print(exclude)
        if selected is None:
            return Response({"error": "No selected image provided."}, status=status.HTTP_400_BAD_REQUEST)

        images = mode.objects.exclude(id__in=exclude)

        if not images.exists():  # Check if the queryset is empty
            qw = session.objects.create(
                info=request.data.get("info"),
                winner=mode.objects.get(id=selected)
            )
            qw.save()
            return Response({"message": "No images available."}, status=status.HTTP_404_NOT_FOUND)
        else:
            a = mode.objects.filter(id=selected)
            if not a.exists():
                return Response({"error": "Selected image does not exist."}, status=status.HTTP_404_NOT_FOUND)
            a.update(score=F('score') + 10)

            random_img = random.choice(images)
            serializer = serializers.ImageModelSerializers(random_img, context={"request": request})
            return Response(serializer.data)

def parse_options(request):
    options = []
    i = 0

    while True:
        option_name_key = f'options[{i}][name]'
        option_image_key = f'options[{i}][image]'

        if option_name_key not in request.data:
            break

        option = {
            'name': request.data.get(option_name_key),
            'image': request.data.get(option_image_key)
        }
        options.append(option)
        i += 1

    return options

class CreateTypeAndModeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        description = request.data.get('description')
        category=request.data.get("category")
        options = parse_options(request)

        print(options)

        cat=Category.objects.get(name=category)
        type_data = {'name': name, 'description': description,'category':cat.id}
        type_serializer = serializers.TypeSerializer(data=type_data)
        if type_serializer.is_valid():
            type_instance = type_serializer.save()
        else:
            return Response(type_serializer.errors, status=status.HTTP_404_NOT_FOUND)

        mode_instances = []
        for option in options:
            mode_data = {'name': option.get('name'), 'img': option.get('image'), 'type': type_instance.id}
            mode_serializer = serializers.ModeSerializer(data=mode_data)
            if mode_serializer.is_valid():
                mode_instance = mode_serializer.save()
                mode_instances.append(mode_instance)
            else:
                type_instance.delete()
                error_response = {'error': f"Invalid data for mode: {mode_serializer.errors}"}
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        response_data = {
            'type': serializers.TypeSerializer(type_instance).data,
            'modes': serializers.ModeSerializer(mode_instances, many=True).data
        }
        return Response( status=status.HTTP_201_CREATED)