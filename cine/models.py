from django.db import models

# Create your models here.
class Tehno(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    owner = models.CharField(max_length=150, blank=True, null=True, default='system')

    def __str__(self):
        return self.title

class Tehno(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=255)
    ratting = models.IntegerField()

    def __str__(self):
        return self.title