from django.db import models


class Note(models.Model):
    def __str__(self):
        return self.id, '.', self.title
    title = models.CharField(max_length=200)

    