from django.db import models
from django.db.models import ForeignKey

from django.core import validators as V

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

    name = models.CharField(max_length=25, null=True, validators=(V.MinLengthValidator(1),))
    surname = models.CharField(max_length=25, null=True, validators=(V.MinLengthValidator(1),))
    email = models.CharField(max_length=100, null=True, validators=[V.validate_email],)
    phone = models.CharField(max_length=12, null=True, validators=(V.MinLengthValidator(3),))
    age = models.IntegerField(validators=(V.MinValueValidator(1),))
    course = models.CharField(max_length=10, null=True)
    course_format = models.CharField(max_length=15, null=True)
    course_type = models.CharField(max_length=100, null=True)
    sum = models.IntegerField(null=True, validators=(V.MinValueValidator(0),))
    alreadyPaid = models.IntegerField(null=True, validators=(V.MinValueValidator(0),))
    created_at = models.DateTimeField(null=True)
    group = models.ForeignKey(GroupModel, on_delete=models.SET_NULL, null=True)
    utm = models.CharField(max_length=100, null=True)
    msg = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=15, null=True)
    manager = models.CharField(max_length=20, null=True)

    objects = OrderManager()


class CommentModel(BaseModel):

    class Meta:
        db_table = 'comments'
        ordering = ('-id',)

    text = models.CharField(max_length=100)
    sender_name = models.CharField(max_length=100, blank=True, null=True)

    order = ForeignKey(OrdersModel, on_delete=models.CASCADE, related_name="messages")
