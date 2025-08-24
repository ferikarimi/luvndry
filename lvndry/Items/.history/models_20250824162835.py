from django.db import models

# Create your models here.


class Items (models.Model) :
    class Meta :
        pass

    name = models.CharField(max_length=255)
    