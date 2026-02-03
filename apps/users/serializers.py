from rest_framework import serializers

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    last_login_display = serializers.SerializerMethodField()

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

    read_only_fields = ('id', 'email', 'is_active', 'is_superuser')

    def get_last_login_display(self, obj):
        if obj.last_login:
            return obj.last_login.strftime("%B %d, %Y")
        else:
            return None


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
