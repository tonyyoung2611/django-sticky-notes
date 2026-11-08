from django.urls import reverse
from django.test import TestCase
from .models import Note


class NoteModelTest(TestCase):

    def setUp(self):
        Note.objects.create(
            title="Test Note",
            content="This is a test note."
        )

    def test_note_has_title(self):
        note = Note.objects.get(title="Test Note")
        self.assertEqual(note.title, "Test Note")

    def test_note_has_content(self):
        note = Note.objects.get(title="Test Note")
        self.assertEqual(note.content, "This is a test note.")


class NoteViewTest(TestCase):

    def setUp(self):
        self.note = Note.objects.create(
            title="Test Note",
            content="This is a test note."
        )

    def test_note_list_view(self):
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")

    def test_note_detail_view(self):
        response = self.client.get(
            reverse("note_detail", args=[self.note.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")
        self.assertContains(response, "This is a test note.")

    def test_note_create_view(self):
        response = self.client.post(
            reverse("note_create"),
            {
                "title": "New Note",
                "content": "This is a new note."
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Note.objects.filter(title="New Note").exists()
        )

    def test_note_update_view(self):
        response = self.client.post(
            reverse("note_update", args=[self.note.id]),
            {
                "title": "Updated Note",
                "content": "This note has been updated."
            }
        )

        self.assertEqual(response.status_code, 302)

        self.note.refresh_from_db()

        self.assertEqual(self.note.title, "Updated Note")
        self.assertEqual(
            self.note.content,
            "This note has been updated."
        )

    def test_note_delete_view(self):
        response = self.client.post(
            reverse("note_delete", args=[self.note.id])
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Note.objects.filter(id=self.note.id).exists()
        )
