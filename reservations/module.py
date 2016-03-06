from django.utils.translation import ugettext_lazy as _

from shoop.admin.base import AdminModule, MenuEntry
from shoop.admin.utils.urls import admin_url


class ReservationsAdminModule(AdminModule):
    name = _("Reservations")
    url = "shoop_admin:reservations.list"
    breadcrumbs_menu_entry = MenuEntry(text=name, url=url)

    def get_urls(self):
        return [
            admin_url(
                "^reservations/new/",
                "reservations.views.ReservationEditView",
                name="reservations.new"
            ),
            admin_url(
                "^reservations/(?P<pk>\d+)",
                "reservations.views.ReservationEditView",
                name="reservations.edit"
            ),
            admin_url(
                "^reservations/",
                "reservations.views.ReservationsAdminList",
                name="reservations.list"
            )
        ]

    def get_menu_entries(self, request):
        return [
            MenuEntry(
                text=self.name, icon="fa fa-calendar",
                url=self.url,
            ),
        ]
