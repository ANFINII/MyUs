from django.db import models


class Product(models.Model):
    name              = models.CharField(max_length=100)
    stripe_product_id = models.CharField(max_length=100)
    price             = models.IntegerField()
    description       = models.TextField(blank=True)
    created           = models.DateTimeField(auto_now_add=True)
    updated           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
