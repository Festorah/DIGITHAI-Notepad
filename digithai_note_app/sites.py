from django.contrib.admin import sites
from django.utils.translation import gettext_lazy as _


class DigiThaiAdminSite(sites.AdminSite):
    site_title = _("DigiThai Admin")
    site_header = _("DigiThai Admin Portal")
    index_title = _("Dashboard")


admin_site = DigiThaiAdminSite()
