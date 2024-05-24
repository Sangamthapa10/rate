from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import mode
from . import serializers
import random
from django.db.models import Count

# Create your views here.


class ImageView(APIView):

    def get(self,request,*args,**kwargs):
        count = mode.objects.count()
        if count < 2:
            return Response({'error': 'Not enough images available'}, status=400)
        random_indices = random.sample(range(count), 2)
        images = [mode.objects.all()[index] for index in random_indices]
        serializer=serializers.ImageModelSerializers(images,context={"request":request},many=True)
        return Response(serializer.data)

    def post(self,request,*args,**kwargs):
        exclude=request.data.get("ids")
        images=mode.objects.exclude(id__in=exclude)
        print(images.count())
        if not images:  # If no images are available after excluding
            return Response({"message": "No images available."}, status=status.HTTP_404_NOT_FOUND)

        random_img=random.choice(images)

        serializer = serializers.ImageModelSerializers(random_img, context={"request": request})
        return Response(serializer.data)




