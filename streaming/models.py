from django.db import models

# Create your models here.

class Stream(models.Model):
    live_at = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=400)

