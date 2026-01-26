from rest_framework import serializers

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    last_login_display = serializers.SerializerMethodField()

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
            'is_active',
            'is_superuser',
            'last_login_display'

        )

    def get_last_login_display(self, obj):
        if obj.last_login:
            return obj.last_login.strftime("%B %d, %Y")
        return None

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
