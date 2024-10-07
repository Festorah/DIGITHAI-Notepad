from rest_framework import serializers
from users.models import AccountUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountUser
        fields = ["email_address", "password", "first_name", "last_name"]
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }

    def create(self, validated_data):
        user = AccountUser(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
            validated_data.pop("password")

        return super().update(instance, validated_data)
