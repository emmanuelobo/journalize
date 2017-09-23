from django.db import models
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField


class Journal(models.Model):
    title = models.CharField(max_length=30)
    text = models.TextField()
    image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    position = GeopositionField()

    class Meta:
        ordering = ['-modified_at']

    def __str__(self):
        return "%s by %s (%s)" % (self.title, self.writer, self.created_at)

    @property
    def location(self):
        '''
        Location of where the entry was posted.
        City, state, and (maybe) zip code.
        :return:
        '''
        pass


    @property
    def mood(self):
        '''
        The overall mood of the entry.
        :return:
        '''
        pass


    @property
    def preview(self):
        '''
        Show a preview of the entry.
        :return:
        '''
        pass