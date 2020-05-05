from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Album(models.Model):
    album_name = models.CharField(max_length=20)
    # album_description = models.CharField(max_length=300)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    is_private= models.BooleanField(default=True)

    def __str__(self):
        return self.album_name

class Picture(models.Model):
    # title = models.CharField(max_length=20, null=True, blank=True)
    picture_file = models.ImageField()
    albums = models.ForeignKey(Album,on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.title


    

    




