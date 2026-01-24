from django.db import models

from core.models import BaseModel


# Create your models here.


class OrdersModel(BaseModel):
    class Meta:
        db_table = 'orders'
        ordering = ('id',)

    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    age = models.IntegerField(blank=True)
    course = models.CharField(max_length=10)
    course_format = models.CharField(max_length=15)
    course_type = models.CharField(max_length=100)
    sum = models.IntegerField(blank=True)
    alreadyPaid = models.IntegerField(blank=True)
    created_at = models.DateTimeField(blank=True)
    utm = models.CharField(max_length=100)
    msg = models.CharField(max_length=100)
    status = models.CharField(max_length=15)
    manager = models.CharField(max_length=20)


