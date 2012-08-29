from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    thumbnail = models.ImageField(upload_to='game_thumbs/', null=True, blank=True)
    link = models.CharField(max_length=256)

class Mod(models.Model):
    game = models.ForeignKey(Game)
    name = models.CharField(max_length=64)
    link = models.CharField(max_length=256)