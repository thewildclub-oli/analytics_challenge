from django.db import models

# Create your models here.

class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    vendor_id = models.IntegerField()
    customer_id = models.IntegerField()

class OrderLine(models.Model):
    order_id = models.IntegerField()
    product_id = models.IntegerField()
    product_description = models.TextField()
    product_price = models.IntegerField()
    product_vat_rate = models.FloatField()
    discount_rate = models.FloatField()
    quantity = models.IntegerField()
    full_price_amount = models.IntegerField()
    discounted_amount = models.FloatField()
    vat_amount = models.FloatField()
    total_amount = models.FloatField()
    
class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField()

class Promotion(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField()

class ProductPromotion(models.Model):
    date = models.DateField()
    product_id = models.IntegerField()
    promotion_id = models.IntegerField()

class VendorCommissions(models.Model):
    date = models.DateField()
    vendor_id = models.IntegerField()
    rate = models.FloatField()
