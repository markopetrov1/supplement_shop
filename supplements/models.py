from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class Supplement(models.Model):
    CATEGORY_CHOICES = [
        ('proteins', 'Proteins'),
        ('creatines', 'Creatines'),
        ('vitamins', 'Vitamins'),
        ('amino-acids', 'Amino Acids'),
        ('pre-workout', 'Pre-Workout')
    ]

    name = models.CharField(max_length=255, null=True, blank=True)

    code = models.CharField(max_length=10, null=True, blank=True)

    brand = models.CharField(max_length=255, null=True, blank=True)

    availability = models.BooleanField(default=True)

    photo = models.ImageField(upload_to='supplements/images', null=True, blank=True)

    description = models.TextField(max_length=2000, null=True, blank=True)

    price = models.IntegerField(null=True, blank=True)

    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, null=True, blank=True)


    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    supplement = models.ForeignKey(Supplement, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True, blank=True)