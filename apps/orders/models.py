from django.db import models
from django.db.models import ForeignKey

from apps.orders.managers import OrderManager
from core.models import BaseModel


class GroupModel(BaseModel):
    class Meta:
        db_table = 'group'
        ordering = ('id',)

    name = models.CharField(max_length=20, unique=True)


class OrdersModel(BaseModel):
    class Meta:
        db_table = 'orders'
        ordering = ('-id',)

    name = models.CharField(max_length=25, blank=True, null=True)
    surname = models.CharField(max_length=25, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    age = models.IntegerField(blank=True)
    course = models.CharField(max_length=10, blank=True, null=True)
    course_format = models.CharField(max_length=15, blank=True, null=True)
    course_type = models.CharField(max_length=100, blank=True, null=True)
    sum = models.IntegerField(blank=True, null=True)
    alreadyPaid = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    group = models.ForeignKey(GroupModel, on_delete=models.SET_NULL, null=True, blank=True)
    utm = models.CharField(max_length=100, blank=True, null=True)
    msg = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=15, blank=True, null=True)
    manager = models.CharField(max_length=20, blank=True, null=True)

    objects = OrderManager()


class MassageModel(BaseModel):

    class Meta:
        db_table = 'comments'
        ordering = ('-id',)

    text = models.CharField(max_length=100)
    sender_name = models.CharField(max_length=100, blank=True, null=True)

    order = ForeignKey(OrdersModel, on_delete=models.CASCADE, related_name="orders", blank=True)