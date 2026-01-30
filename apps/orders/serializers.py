from rest_framework import serializers

from django.db import models

from apps.orders.models import OrdersModel, GroupModel, CommentModel


class OrdersSerializer(serializers.ModelSerializer):
    created_date = serializers.SerializerMethodField()
    comments_count = serializers.IntegerField(read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=GroupModel.objects.all(),
        source="group",
        write_only=True,
        required=False,
        allow_null=True
    )

    group = serializers.CharField(source="group.name", read_only=True)

    class Meta:
        model = OrdersModel
        fields = ('id', 'name', 'surname',  'email', 'phone', 'age', 'course', 'course_format', 'course_format', 'course_type', 'sum', 'alreadyPaid', 'group', 'created_at', 'created_date', 'utm', 'msg', 'status', 'manager', 'group_id', 'comments_count')
        read_only_fields = ('id', 'created_at', 'comments_count')

    def get_created_date(self, obj):
        if obj.created_at:
            return obj.created_at.strftime("%B %d, %Y")
        return None

    def validate(self, attrs):
        for field_name, value in attrs.items():
            model_field = self.Meta.model._meta.get_field(field_name)
            if isinstance(model_field, (models.CharField, models.TextField)) and value == "":
                attrs[field_name] = "null"
        return attrs


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupModel
        fields = ('id', 'name')
        read_only_fields = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    created_date = serializers.SerializerMethodField()
    order_id = serializers.IntegerField(source='order.id', read_only=True)

    class Meta:
        model = CommentModel
        fields = ('id', 'sender_name', 'created_date', 'text', 'order_id')
        read_only_fields = ('id', 'order_id')

    def get_created_date(self, obj):
        if obj.created_at:
            return obj.created_at.strftime("%B %d, %Y")
        return None
