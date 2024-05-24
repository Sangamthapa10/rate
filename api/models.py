from django.db import models

# Create your models here.

class mode(models.Model):
    name=models.CharField(blank=True,max_length=100)
    img=models.ImageField(upload_to="images/")



class session(models.Model):
    id=models.AutoField(primary_key=True)

