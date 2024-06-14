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
    price=models.FloatField(default=0.0)
    discount_price=models.FloatField(default=0.0)
    class Meta:
        unique_together = ('tag', 'category')

class woocomerceuser(models.Model):
    consumer_key=models.CharField(max_length=1000,default="default value")
    secret_key=models.CharField(max_length=1000,default="default value")
    active = models.BooleanField(default=False)
    class Meta:
        unique_together = ('consumer_key', 'secret_key')

class integrate(models.Model):
    type=models.CharField(max_length=255,default="default value")
    consumer_key=models.CharField(max_length=1000,default="default value")
    secret_key=models.CharField(max_length=1000,default="default value")
    active = models.BooleanField(default=False)
    name = models.CharField(max_length=255, default="Integration Name")
    description = models.CharField(max_length=100,default="default value")




    



