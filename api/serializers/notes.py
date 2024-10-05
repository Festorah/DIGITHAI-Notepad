from core.models import Note
from rest_framework import serializers


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at"]

    # Ensure the note's user is the request's authenticated user
    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)
