from django.urls import path

from .views import CreateNoteView, HomeView, NoteDeleteView, NoteDetailEditView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("note/create", CreateNoteView.as_view(), name="create_note"),
    path(
        "note/<uuid:pk>/delete/",
        NoteDeleteView.as_view(),
        name="note_delete",
    ),
    path("note/<uuid:pk>/", NoteDetailEditView.as_view(), name="note_detail"),
]
