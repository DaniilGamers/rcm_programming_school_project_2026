from rest_framework import serializers

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = UserModel
        fields = (
            'id',
            'email',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
            'is_banned',
            'created_at',
            'updated_at'

        )
        read_only_fields = ('user_id', 'is_active', 'is_staff', 'is_superuser', 'created_at')
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }