from django.db import models

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    players_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
