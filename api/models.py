from django.db import models

# Create your models here.

class mode(models.Model):
    name=models.CharField(blank=True,max_length=100)
    img=models.ImageField(upload_to="images/")
    score=models.IntegerField(default=0)



class session(models.Model):
    id=models.AutoField(primary_key=True)
    info=models.CharField(max_length=300)
    winner=models.ForeignKey(mode,on_delete=models.CASCADE)

