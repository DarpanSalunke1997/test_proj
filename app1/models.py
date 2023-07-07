from django.db import models


# Create your models here.
class NewModel(models.Model):
    name = models.CharField(default="", max_length=150, null=True, blank=True)
    email = models.EmailField(default="", max_length=150, null=True, blank=True)
    pnumber = models.CharField(default="", max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name
