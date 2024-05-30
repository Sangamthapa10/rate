from django.db import models

# Create your models here.



class Category(models.Model):
    name=models.CharField(max_length=100)

class Type(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    default=models.BooleanField(default=False)
    status=models.BooleanField(default=True)
    dp=models.ImageField(upload_to="images/",null=True,blank=True)
    description=models.TextField(max_length=200,null=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
class mode(models.Model):
    name=models.CharField(blank=True,max_length=100)
    img=models.ImageField(upload_to="images/")
    score=models.IntegerField(default=0)
    type=models.ForeignKey(Type,on_delete=models.CASCADE,blank=True,null=True)
    status=models.BooleanField(default=True)





class session(models.Model):
    id=models.AutoField(primary_key=True)
    info=models.CharField(max_length=300)
    winner=models.ForeignKey(mode,on_delete=models.CASCADE)

