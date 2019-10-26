from django.db import models

# Create your models here.
class Store(models.Model):
    id_code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    phone = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)+" "\
               +self.id_code+" "\
               +self.name+" "\
               +self.address+" "\
               +str(self.latitude)+" "\
               +str(self.longitude)+" "\
               +self.phone



class Products(models.Model):
    store = models.ForeignKey('Store', on_delete=models.DO_NOTHING, default=None)
    id_code = models.CharField(max_length=100)
    tags = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    count = models.FloatField()
    price = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    discount_price = models.FloatField(default=0)

    def __str__(self):
        return str(self.store.id)+" "\
               +str(self.id_code)+" "\
               +str(self.name)+" "\
               +str(self.image)+" "\
               +str(self.date)+" "\
               +str(self.count)


class Wish(models.Model):
    id_code = models.CharField(max_length=100, default="")
    category = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    needCount = models.FloatField()
    existCount = models.FloatField()

    def __str__(self):
        return str(self.id_code) + " " \
               + str(self.category) + " " \
               + str(self.date) + " " \
               + str(self.needCount) + " " \
               + str(self.existCount)

class Order(models.Model):
    product = models.CharField(max_length=100)
    count = models.FloatField()
    date = models.CharField(max_length=100)
    qr = models.CharField(max_length=100)
    status = models.BooleanField(default=False)