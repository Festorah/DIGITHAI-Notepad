from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import NoteForm, NoteUpdateForm
from .models import Note


class DateRange:
    TODAY = "today"
    YESTERDAY = "yest"
    LAST_WEEK = "last-week"
    LAST_MONTH = "last-month"


class HomeView(LoginRequiredMixin, CreateView, ListView):
    model = Note
    template_name = "core/home.html"
    context_object_name = "notes"
    form_class = NoteForm
    success_url = reverse_lazy("home")
    login_url = reverse_lazy("login")
    paginate_by = 5

    def get_queryset(self):
        # Initialize the base queryset
        queryset = (
            Note.objects.all().filter(author=self.request.user).order_by("-created_at")
        )
        search_query = self.request.GET.get("search_note", "").strip()
        date_type = self.request.GET.get("type", "")

        filters = Q()

        # Add filters based on search query
        if search_query:
            filters &= Q(title__icontains=search_query) | Q(
                content__icontains=search_query
            )

        # Add date filters based on selected type
        if date_type:
            filters &= self.get_date_filter(date_type)

        return queryset.filter(filters)

    def get_date_filter(self, date_type):
        today = timezone.now().date()
        if date_type == DateRange.TODAY:
            return Q(created_at__date=today)
        elif date_type == DateRange.YESTERDAY:
            return Q(created_at__date=today - timedelta(days=1))
        elif date_type == DateRange.LAST_WEEK:
            return Q(created_at__date__gte=today - timedelta(weeks=1))
        elif date_type == DateRange.LAST_MONTH:
            return Q(created_at__date__gte=today - timedelta(days=30))

        # Return an empty Q object if no valid date type
        return Q()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["search_query"] = self.request.GET.get("search", "").strip()
        context["date_type"] = self.request.GET.get("type", "")
        return context

    def form_valid(self, form):
        # Save the note with the current logged-in user as the author
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = "core/details_page.html"
    context_object_name = "note"
    login_url = reverse_lazy("login")

    def get_object(self, queryset=None):
        note = super().get_object(queryset)
        if note.author != self.request.user:
            raise Http404("You are not allowed to view this note.")
        return note


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteUpdateForm
    template_name = "core/details_page.html"
    context_object_name = "note"
    login_url = reverse_lazy("login")

    def get_object(self, queryset=None):
        note = super().get_object(queryset)
        if note.author != self.request.user:
            raise Http404("You are not allowed to edit this note.")
        return note

    def get_success_url(self):
        return reverse_lazy("note_detail", kwargs={"pk": self.object.pk})


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = "note_confirm_delete.html"
    success_url = reverse_lazy("home")
    login_url = reverse_lazy("login")

    def get_object(self, queryset=None):
        note = super().get_object(queryset)
        if note.author != self.request.user:
            raise Http404("You are not allowed to delete this note.")
        return note


class NoteDetailEditView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "core/details_page.html"
    context_object_name = "note"

    def get_success_url(self):
        return reverse_lazy("note_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["edit_mode"] = self.request.GET.get("edit", False)
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    # Ensure users can only view/edit their own notes
    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)


class CreateNoteView(LoginRequiredMixin, TemplateView):
    template_name = "core/create_new_note.html"

    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = NoteForm()
        return context
