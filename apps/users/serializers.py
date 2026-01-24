from rest_framework import serializers

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True)
    surname = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:

        model = UserModel
        fields = (
            'id',
            'email',
            'name',
            'surname',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login'

        )
        read_only_fields = ('id', 'email', 'name', 'surname', 'is_active', 'last_login')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': False,
                'allow_blank': True
            },
        }


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )
    password_confirm = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs
