from api.permissions import IsOwner
from api.serializers import NoteSerializer
from core.models import Note
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated


class NoteViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions to list, create, retrieve,
    update, and delete notes. It only allows authenticated users to interact
    with their own notes.
    """

    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Ensure users only see their own notes
        return Note.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        # Set the user to the logged-in user
        serializer.save(author=self.request.user)

    # Add filtering capabilities
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content"]  # Allow filtering by title or content
    ordering_fields = ["created_at"]  # Allow ordering by date
    ordering = ["-created_at"]  # Default ordering by most recent
