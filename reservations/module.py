from django.utils.translation import ugettext_lazy as _
from shoop.admin.base import AdminModule, MenuEntry


class ReservationsAdminModule(AdminModule):
    name = _("Reservations")
    category = name

    def get_menu_entries(self, request):
        return [
            MenuEntry(
                text=_("Reservations"), icon="fa fa-calendar",
                url="reservations:reservations.list",
                category=self.category
            ),
        ]
