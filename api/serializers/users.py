from rest_framework import serializers
from users.models import AccountUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountUser
        fields = ["email_address", "password", "first_name", "last_name"]

    def create(self, validated_data):
        user = AccountUser(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
