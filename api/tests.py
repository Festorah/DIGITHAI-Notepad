import json
from datetime import timedelta

from core.models import Note
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from users.models import AccountUser


class NotesAPITestCase(APITestCase):
    def setUp(self):
        """
        Initialize test data for the Notes API.
        This will create a test user and test notes.
        """
        self.client = APIClient()
        # Create users
        self.user = AccountUser.objects.create_user(
            email_address="testuser@example.com", password="password123"
        )
        self.other_user = AccountUser.objects.create_user(
            email_address="otheruser@example.com", password="password456"
        )

        # Get JWT token for authentication
        response = self.client.post(
            reverse("api-login"),
            data={"email_address": "testuser@example.com", "password": "password123"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.data["access"]

        # Set Authorization header for future requests
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        # Create notes for user
        self.note = Note.objects.create(
            title="Sample Note 1",
            content="This is the content of sample note 1.",
            author=self.user,
            created_at=timezone.now() - timedelta(days=1),
        )
        self.note2 = Note.objects.create(
            title="Sample Note 2",
            content="This is the content of sample note 2.",
            author=self.user,
            created_at=now(),
        )
        self.other_note = Note.objects.create(
            title="Other User Note",
            content="This is another note by another user.",
            author=self.other_user,
            created_at=now(),
        )

        # URL endpoints
        self.notes_url = reverse("note-list")
        self.note_detail_url = reverse("note-detail", kwargs={"pk": self.note.pk})

    def test_register_user(self):
        """Test user registration"""
        response = self.client.post(
            reverse("register"),
            data={
                "email_address": "newuser@example.com",
                "password": "password789",
                "first_name": "New",
                "last_name": "User",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            AccountUser.objects.filter(email_address="newuser@example.com").exists()
        )

    def test_login_user(self):
        """Test user login"""
        response = self.client.post(
            reverse("api-login"),
            data={"email_address": "testuser@example.com", "password": "password123"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_unauthenticated_access(self):
        """Ensure unauthenticated users cannot access notes"""
        self.client.logout()
        response = self.client.get(self.notes_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_note(self):
        """Test creating a note"""
        data = {"title": "New Note", "content": "This is a new note."}
        response = self.client.post(self.notes_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.filter(author=self.user).count(), 3)

    def test_retrieve_note(self):
        """Test retrieving a note"""
        response = self.client.get(self.note_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.note.title)

    def test_update_note(self):
        """Test updating a note"""
        data = {"title": "Updated Note", "content": "Updated content of the note."}
        response = self.client.put(self.note_detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Updated Note")
        self.assertEqual(self.note.content, "Updated content of the note.")

    def test_delete_note(self):
        """Test deleting a note"""
        response = self.client.delete(self.note_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_permission_denied_on_other_user_note(self):
        """Test that a user cannot access or modify another user's note"""
        other_note_url = reverse("note-detail", kwargs={"pk": self.other_note.pk})

        # Try to retrieve another user's note
        response = self.client.get(other_note_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try to update another user's note
        data = {"title": "Should not update", "content": "Unauthorized update"}
        response = self.client.put(other_note_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try to delete another user's note
        response = self.client.delete(other_note_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_notes(self):
        """Test searching notes by title and content"""
        # Search for a note by title
        response = self.client.get(self.notes_url, {"search": "Sample Note 1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Sample Note 1")

        # Search for a note by content
        response = self.client.get(
            self.notes_url, {"search": "content of sample note 1"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["content"],
            "This is the content of sample note 1.",
        )

    def test_order_notes_by_created_at(self):
        """Test ordering notes by creation date"""
        response = self.client.get(self.notes_url, {"ordering": "-created_at"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notes = json.loads(response.content)
        self.assertTrue(
            notes["results"][0]["created_at"] > notes["results"][1]["created_at"]
        )

    def test_note_creation_with_empty_fields(self):
        """Test creating a note with empty title or content"""
        data = {"title": "", "content": ""}
        response = self.client.post(self.notes_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_note_creation_with_long_content(self):
        """Test creating a note with excessive content"""
        data = {"title": "Long Note", "content": "A" * 10000}
        response = self.client.post(self.notes_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Note.objects.filter(title="Long Note").exists())

    def test_retrieve_nonexistent_note(self):
        """Test retrieving a non-existing note"""
        response = self.client.get(reverse("note-detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_note(self):
        """Test updating a non-existing note"""
        response = self.client.put(
            reverse("note-detail", kwargs={"pk": 999}), data={"title": "Does not exist"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_note(self):
        """Test deleting a non-existing note"""
        response = self.client.delete(reverse("note-detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
