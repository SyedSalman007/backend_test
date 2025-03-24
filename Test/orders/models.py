from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
  email = models.EmailField(unique=True)
  groups = models.ManyToManyField(
        "auth.Group",
        related_name="orders_user_set",  # Unique related_name
        blank=True
    )
  user_permissions = models.ManyToManyField(
      "auth.Permission",
      related_name="orders_user_permissions_set",  # Unique related_name
      blank=True
  )

class Orders(models.Model):
  email = models.EmailField()
  product_name = models.CharField(max_length=100)
  product_price = models.DecimalField(max_digits=10, decimal_places=2)
  quantity = models.IntegerField()
  order_date = models.DateTimeField(auto_now_add=True)