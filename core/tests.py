from core.models import Note
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from users.models import AccountUser


class NoteAppTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = AccountUser.objects.create_user(
            email_address="digithaiadmin@gmail.com", password="testpass"
        )
        self.client.login(email_address="digithaiadmin@gmail.com", password="testpass")

        # Create sample notes
        self.note1 = Note.objects.create(
            title="Test Note 1",
            content="Content for note 1",
            author=self.user,
            created_at=timezone.now(),
        )
        self.note2 = Note.objects.create(
            title="Test Note 2",
            content="Content for note 2",
            author=self.user,
            created_at=timezone.now() - timezone.timedelta(days=1),
        )

    def tearDown(self):
        # Clean up after tests
        Note.objects.all().delete()
        AccountUser.objects.all().delete()


class HomeViewTests(NoteAppTests):

    def test_home_page_access(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")

    def test_notes_displayed(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, self.note1.title)
        self.assertContains(response, self.note2.title)

    def test_pagination(self):
        # Create additional notes to trigger pagination
        for i in range(10):
            Note.objects.create(
                title=f"Note {i+3}",
                content=f"Content for note {i+3}",
                author=self.user,
                created_at=timezone.now(),
            )

        response = self.client.get(reverse("home"))
        self.assertEqual(len(response.context["notes"]), 5)

    def test_search_filter(self):
        response = self.client.get(reverse("home"), {"search_note": "Test Note 1"})
        self.assertContains(response, self.note1.title)
        self.assertNotContains(response, self.note2.title)


class CreateNoteViewTests(NoteAppTests):

    def test_create_note_access(self):
        response = self.client.get(reverse("create_note"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/create_new_note.html")

    def test_create_note_post(self):
        note_data = {
            "title": "New Note",
            "content": "New note content",
        }
        response = self.client.post(reverse("home"), data=note_data)
        self.assertEqual(
            response.status_code, 302
        )  # Redirects after successful creation
        self.assertTrue(Note.objects.filter(title="New Note").exists())


class NoteDetailViewTests(NoteAppTests):

    def test_note_detail_view(self):
        response = self.client.get(reverse("note_detail", kwargs={"pk": self.note1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/details_page.html")
        self.assertContains(response, self.note1.title)

    def test_note_detail_permission(self):
        other_user = AccountUser.objects.create_user(
            email_address="otheruser", password="pass"
        )
        self.client.login(email_address="otheruser", password="pass")
        response = self.client.get(reverse("note_detail", kwargs={"pk": self.note1.pk}))

        # Other users must not be able to view this note
        self.assertEqual(response.status_code, 404)


class NoteUpdateViewTests(NoteAppTests):

    def test_update_note_view(self):
        update_data = {
            "title": "Updated Title",
            "content": "Updated content",
        }
        response = self.client.post(
            reverse("note_detail", kwargs={"pk": self.note1.pk}), data=update_data
        )
        self.assertEqual(response.status_code, 302)
        self.note1.refresh_from_db()
        self.assertEqual(self.note1.title, "Updated Title")


class NoteDeleteViewTests(NoteAppTests):

    def test_delete_note_view(self):
        response = self.client.post(
            reverse("note_delete", kwargs={"pk": self.note1.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(pk=self.note1.pk).exists())
