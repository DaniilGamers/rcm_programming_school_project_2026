from rest_framework import serializers

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    last_login_display = serializers.DateTimeField(
        source='last_login',
        read_only=True,
        format='%B %d, %Y')

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

    read_only_fields = ('id', 'email', 'is_active', 'is_superuser', 'last_login_display')


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        if password != password_confirm:
            raise serializers.ValidationError({
                "password_confirm": "Passwords do not match"
            })
        return attrs

    def save(self):
        user = self.context["user"]

        user.set_password(self.validated_data["password"])
        user.is_active = True
        user.save()

        return user
