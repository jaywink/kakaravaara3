# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from reservable_pricing.models import PeriodPriceModifier
from reservations.notify_events import ReservationsOrderReceived, get_order_details
from shoop.core.models import Product, Order, OrderLine
from shoop.core.models._orders import OrderStatusRole
from shoop.front.signals import order_creator_finished


class ReservableProduct(models.Model):
    """Products that have reservable properties."""

    product = models.OneToOneField(Product, verbose_name=_(u"reservable product"), related_name="reservable")
    check_out_time = models.TimeField(verbose_name=_(u"sign out time"), default=datetime.time(hour=12))
    check_in_time = models.TimeField(verbose_name=_(u"sign in time"), default=datetime.time(hour=15))
    available_count = models.IntegerField(verbose_name=_(u"available quantity"), default=1)
    pricing_per_person = models.BooleanField(verbose_name=_("pricing per person"), default=False)
    pricing_per_person_included = models.PositiveIntegerField(
        verbose_name=_("people included in price"), null=True, blank=True,
    )
    pricing_per_person_price = models.DecimalField(
        verbose_name=_("price per person"), null=True, blank=True, decimal_places=2, max_digits=6,
    )
    sort_order = models.PositiveIntegerField(verbose_name=_(u"sort order"), default=50)

    class Meta:
        verbose_name = _('reservable product')
        verbose_name_plural = _('reservable products')
        ordering = ("sort_order",)

    def __str__(self):
        return self.product.safe_translation_getter("name") or self.product.sku

    def get_reserved_dates(self, start, end):
        """Get a list of reserved dates, between and including start and end.

        Args:
            start (date)
            end (date)

        Returns:
            list of dates or []
        """
        return Reservation.get_reserved_days_for_period(start, end, self)

    def is_period_days_free(self, start, end):
        """Check if period is free."""
        return len(self.get_reserved_dates(start, end)) == 0

    @property
    def has_price_modifiers(self):
        """Check if this reservable has price modifiers.

        Returns:
            True or False
        """
        if self.pricing_per_person:
            return True
        if self.period_price_modifiers.exists():
            return True
        return False

    @property
    def period_price_modifiers(self):
        future_period_modifiers = PeriodPriceModifier.objects.filter(
            product=self.product, start_date__gte=datetime.date.today()).order_by("start_date")
        return future_period_modifiers


class Reservation(models.Model):
    """A single reservation."""

    reservable = models.ForeignKey(
        ReservableProduct, verbose_name=_(u"reservable product"), related_name="reservations")
    order_line = models.OneToOneField(
        OrderLine, verbose_name=_("order line"), related_name="reservation", null=True, blank=True)
    start_time = models.DateTimeField(verbose_name=_(u"starts"))
    end_time = models.DateTimeField(verbose_name=_(u"ends"))
    persons = models.IntegerField(verbose_name=_(u"persons"), default=1)

    class Meta:
        verbose_name = _('reservation')
        verbose_name_plural = _('reservations')

    def __str__(self):
        return str(self.reservable)

    def save(self, *args, **kwargs):
        # Validate end_time is past start_time
        if self.end_time <= self.start_time:
            raise ValueError
        return super(Reservation, self).save(*args, **kwargs)

    @staticmethod
    def get_reserved_days_for_period(start_date, end_date, reservable=None):
        """Get a list of reserved dates, between and including start and end.

        Args:
            start_date (date)
            end_date (date)
            reservable (ReservableProduct, optional)    - optionally filter by reservable

        Returns:
            list of dates or []
        """
        reservations = Reservation.objects.filter(
            start_time__gte=start_date, end_time__lte=end_date,
        )
        reservations = reservations | Reservation.objects.filter(
            Q(start_time__range=(start_date, end_date)) | Q(end_time__range=(start_date, end_date))
        )
        reservations = reservations | Reservation.objects.filter(
            (
                Q(start_time__lt=start_date) & Q(end_time__gte=start_date)
            ) |
            (
                Q(start_time__lte=end_date) & Q(end_time__gt=end_date)
            )
        )
        if reservable:
            reservations = reservations.filter(reservable=reservable)
        dates = []
        for reservation in reservations.distinct():
            current = max(reservation.start_time.date(), start_date)
            while current < reservation.end_time.date() and current <= end_date:
                dates.append(current)
                current += datetime.timedelta(days=1)
        return dates


@receiver(order_creator_finished)
def send_order_received_notification(sender, **kwargs):
    order = kwargs["order"]
    request = kwargs["request"]
    ReservationsOrderReceived(
        order=order,
        order_id=order.id,
        order_details=get_order_details(order),
        order_url="%s%s" % (
            settings.KAKARAVAARA_SITE_URL, reverse("shoop:order_complete", kwargs={"pk": order.pk, "key": order.key})
        ),
        customer_email=order.email,
        customer_phone=order.phone,
        customer_name=order.billing_address.name if order.billing_address else "",
        language=request.LANGUAGE_CODE,
        additional_notes=order.customer_comment,
        total_sum=order.taxful_total_price_value,
    ).run()


@receiver(post_save, sender=Order)
def order_post_save(sender, instance, **kwargs):
    if instance.status.role == OrderStatusRole.CANCELED:
        reservations = Reservation.objects.filter(order_line__order=instance)
        for reservation in reservations:
            reservation.delete()
