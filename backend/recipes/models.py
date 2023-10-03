from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    units = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
