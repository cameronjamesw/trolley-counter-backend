from django.db import models
from django.contrib.auth.models import User
from api.models import Trolley

# Create your models here.

class Pinned(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    trolley = models.ForeignKey(
        Trolley, related_name='favourites', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['creator', 'trolley']

    def __str__(self):
        return f'{self.creator}, {self.trolley}'
