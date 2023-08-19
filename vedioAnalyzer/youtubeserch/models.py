from django.db import models

# Create your models here.
class PersonDetail(models.Model):
    name = models.CharField(max_length=16)
    lname = models.CharField(max_length=16)
    fatherName = models.CharField(max_length=16)
    address = models.CharField(max_length=30)

    def __str__(self):
        return self.name.capitalize()
    
