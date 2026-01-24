from rest_framework import serializers

from apps.orders.models import OrdersModel


class OrdersSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrdersModel
        fields = ('id', 'name', 'surname',  'email', 'phone', 'age', 'course', 'course_format', 'course_format', 'course_type', 'sum', 'alreadyPaid', 'created_at', 'utm', 'msg', 'status')
        read_only_fields = ('id', 'created_at')
