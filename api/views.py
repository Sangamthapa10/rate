from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import mode, session
from . import serializers
import random
from django.db.models import Count, F


class ImageView(APIView):

    def get(self, request, *args, **kwargs):
        count = mode.objects.count()
        if count < 2:
            return Response({'error': 'Not enough images available'}, status=status.HTTP_400_BAD_REQUEST)

        random_indices = random.sample(range(count), 2)
        images = [mode.objects.all()[index] for index in random_indices]
        serializer = serializers.ImageModelSerializers(images, context={"request": request}, many=True)

        top=mode.objects.order_by('-score')[:5]
        serializerq = serializers.ImageModelSerializers(top, context={"request": request}, many=True)
        data={
            'a':serializer.data,
            'b':serializerq.data
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
