from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    stock = models.PositiveIntegerField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places =2)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name}"
    
