from shoop.apps import AppConfig


class ReservationsAppConfig(AppConfig):
    name = "reservations"
    verbose_name = "Reservations"
    label = "reservations"

    provides = {
        "admin_module": [
            "reservations.module:ReservationsAdminModule"
        ]
    }
