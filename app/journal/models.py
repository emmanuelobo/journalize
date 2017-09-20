from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Journal(models.Model):
    title = models.CharField(max_length=30)
    text = models.TextField()
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=False)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return "%s by %s (%s)" % (self.title, self.writer, self.created_at)