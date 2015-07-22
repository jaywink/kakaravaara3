from calendar import monthrange
from babel.dates import format_datetime
from datetime import date, timedelta, datetime
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.utils.timezone import localtime
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from shoop.admin.modules.products.views import ProductEditView
from shoop.admin.toolbar import URLActionButton
from shoop.admin.utils.picotable import Column, TextFilter
from shoop.admin.utils.views import PicotableListView, CreateOrUpdateView
from shoop.front.views.product import ProductDetailView
from shoop.utils.i18n import get_current_babel_locale

from reservations.forms import ReservableDatesForm, ReservableProductFormPart
from reservations.models import Reservation, ReservableProduct


class ReservableProductDetailView(ProductDetailView):

    def get_context_data(self, **kwargs):
        context = super(ReservableProductDetailView, self).get_context_data(**kwargs)

        if self.object.type.identifier == "reservable":
            # Add form for date inputs
            context["reservable_dates_form"] = ReservableDatesForm()

        return context

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        if product.type.identifier == "reservable":
            # Use our template for reservables
            self.template_name = "reservations/reservable_product.jinja"

        return super(ReservableProductDetailView, self).get(request, *args, **kwargs)


class ReservableProductEditView(ProductEditView):

    def get_form_part_classes(self):
        form_part_classes = super(ReservableProductEditView, self).get_form_part_classes()
        if self.object.type.identifier == "reservable":
            form_part_classes.append(ReservableProductFormPart)
        return form_part_classes

    def get_toolbar(self):
        toolbar = super(ReservableProductEditView, self).get_toolbar()
        if hasattr(self.object, "reservable") and self.object.pk:
            toolbar.append(URLActionButton(
                text=_("Reservations"),
                icon="fa fa-calendar-o",
                url=reverse("reservations:product.reservations", kwargs={"pk": self.object.reservable.pk}),
            ))
        return toolbar


class ReservableReservationsListView(PicotableListView):
    model = Reservation
    columns = [
        Column(
            "name", _("Name"), sort_field="reservable__product__translations__name",
            display="reservable__product__name",
            filter_config=TextFilter(
                filter_field="reservable__product__translations__name",
                placeholder=_("Filter by reservable..."))
        ),
        Column("order", _("From Order"), sort_field="order", display="order"),
        Column("start_time", _("Sign In Time"), sort_field="start_time", display="format_start_time"),
        Column("end_time", _("Sign Out Time"), sort_field="end_time", display="format_end_time"),
        Column("adults", _("Adults"), display="adults"),
        Column("children", _("Children"), display="children"),
    ]

    def format_start_time(self, instance, *args, **kwargs):
        return format_datetime(localtime(instance.start_time), locale=get_current_babel_locale())

    def format_end_time(self, instance, *args, **kwargs):
        return format_datetime(localtime(instance.end_time), locale=get_current_babel_locale())

    def get_queryset(self):
        return Reservation.objects.filter(reservable__id=self.reservable_id)

    def get_toolbar(self):
        toolbar = super(ReservableReservationsListView, self).get_toolbar()
        toolbar.append(URLActionButton(
            text=_("New Reservation"),
            icon="fa fa-calendar",
            url=reverse("reservations:product.reservations.new", kwargs={"reservable": self.reservable_id}),
        ))
        return toolbar

    def get(self, request, *args, **kwargs):
        self.reservable_id = kwargs.get("pk")
        return super(ReservableReservationsListView, self).get(request, *args, **kwargs)

    def get_object_url(self, instance):
        return reverse(
            "reservations:product.reservations.edit", kwargs={"reservable": self.reservable_id, "pk": instance.id})


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        exclude = ()


class ReservationEditView(CreateOrUpdateView):
    model = Reservation
    template_name = "reservations/reservation_edit.jinja"
    context_object_name = "reservation"
    form_class = ReservationForm


class ReservableSearchView(TemplateView):
    template_name = "reservations/reservable_search.jinja"

    def get(self, request, *args, **kwargs):
        start = request.GET.get("start", None)
        end = request.GET.get("end", None)
        if not start:
            self.start_date = date(date.today().year, date.today().month, 1)
            self.end_date = self.start_date + timedelta(days=40)
        else:
            self.start_date = datetime.strptime(start, "%Y-%m-%d")
            self.start_date = self.start_date.replace(day=1)
            self.end_date = datetime.strptime(end, "%Y-%m-%d")
        self.end_date = date(
            self.end_date.year, self.end_date.month, monthrange(self.end_date.year, self.end_date.month)[1]
        )
        return super(ReservableSearchView, self).get(request, *args, **kwargs)

    def _get_reservables(self):
        return ReservableProduct.objects.all()

    def _get_reserved_days_as_strings(self):
        reservables = self._get_reservables()
        reserved_days = {}
        for reservable in reservables:
            days = Reservation.get_reserved_days_for_period(self.start_date, self.end_date, reservable)
            day_list = []
            for day in days:
                day_list.append("%s" % day.strftime("%Y-%m-%d"))
            reserved_days[reservable.product.sku] = day_list
        return reserved_days

    def get_context_data(self, **kwargs):
        context = super(ReservableSearchView, self).get_context_data(**kwargs)
        context["reservables"] = self._get_reservables()
        context["start_date"] = self.start_date.strftime("%Y-%m-%d")
        context["end_date"] = self.end_date.strftime("%Y-%m-%d")
        context["reserved_days"] = self._get_reserved_days_as_strings()

        # calculate months
        months = []
        # to not end up in endless loop
        assert self.end_date.month >= self.start_date.month and self.end_date.year >= self.start_date.year
        current = self.start_date
        while True:
            months.append(current.strftime("%Y-%m-01"))
            if self.end_date.month != current.month or self.end_date.year != current.year:
                # not super correct but enough
                current = current + timedelta(days=32)
            else:
                break
        context["months"] = months
        return context
