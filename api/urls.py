from django.urls import path
from . import views

app_name='api'

urlpatterns=[
    path("img/<int:id>/",views.ImageView.as_view()),
    path('create/',views.CreateTypeAndModeAPIView.as_view())


]