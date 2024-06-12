from django.db import models
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100,default="default value")
    description=models.CharField(max_length=100,default="default value")

class Tag(models.Model):
    name = models.CharField(max_length=100,default="default value")
    description=models.CharField(max_length=100,default="default value")

class Item(models.Model):
    name = models.CharField(max_length=255,default="default value")
    description = models.CharField(max_length=100,default="default value")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE,related_name="items")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="items")
    weight = models.FloatField(default=0.0)
    brand = models.CharField(max_length=100, default="default value")
    class Meta:
        unique_together = ('tag', 'category')



