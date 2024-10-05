from core.models import Note
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from users.models import AccountUser

from digithai_note_app.sites import admin_site


@admin.register(AccountUser, site=admin_site)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email_address",
        "is_active",
        "first_name",
        "last_name",
    )
    list_display_links = ("id",)


@admin.register(Note, site=admin_site)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "title",
    )
    list_display_links = ("id",)
