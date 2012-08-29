from django.db import models

# Create your models here.
class Setting(models.Model):
    name = models.CharField(max_length=64)
    value = models.CharField(max_length=64)

    def __unicode__(self):
        return '%s : %s' % (self.name, self.value)