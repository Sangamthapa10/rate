from django.urls import path
from . import views

app_name='api'

urlpatterns=[
    path("img/",views.ImageView.as_view())

]