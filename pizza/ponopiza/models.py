from django.db import models

# Create your models here.
class category(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return( f"{self.name}")
class items(models.Model):
    itemsname = models.CharField(max_length=64)
    cat = models.ForeignKey(category,on_delete=models.CASCADE,related_name="itemslist")
    topngNO = models.IntegerField()
    small = models.FloatField()
    large = models.FloatField()
    def __str__(self):
        return(f"{self.itemsname},{self.topngNO},{self.small},{self.large}")
class toppings(models.Model):
    toppingname = models.CharField(max_length=64)
    item = models.ManyToManyField(items,blank=True,related_name="toppings")
    def __str__(self):
        return(f"{self.toppingname}")
class placedorders(models.Model):
    orderuser=models.CharField(max_length=64)
    ordername = models.CharField(max_length=64)
    size= models.CharField(max_length=64)
    price=models.IntegerField()
    def __str__(self):
        return(f"{self.ordername},{self.size},{self.price},{self.orderuser}")
class placedtoppings(models.Model):
    ordertoppingname = models.CharField(max_length=64)
    order = models.ManyToManyField(placedorders,blank=True,related_name="placedtoppings")
    def __str__(self):
        return(f"{self.ordertoppingname}")
